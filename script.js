// ============================================
// Detección de rostro + emoción con face-api.js
// Cuando detecta tristeza reproduce un video
// Se detiene cuando dejas de estar triste
// ============================================

let video;
let canvas;
let sadVideo;
let sadnessTimeout = null;
let isShowingVideo = false;
let isShowingCinnamonroll = false;
let detectionInterval = null;
let happyFrames = 0;
let smileFrames = 0;
let noSmileFrames = 0;
const HAPPY_FRAMES_NEEDED = 6; // ~3s (6 frames × 500ms)
const SMILE_FRAMES_NEEDED = 3; // ~1.5s para mostrar Cinnamonroll
const NO_SMILE_FRAMES_NEEDED = 6; // ~3s para ocultar Cinnamonroll

async function init() {
    video = document.getElementById('camera-feed');
    canvas = document.getElementById('overlay-canvas');
    sadVideo = document.getElementById('sad-video');

    const statusEl = document.getElementById('camera-status');
    statusEl.textContent = 'Cargando modelos de IA...';

    try {
        // Verificar que face-api.js cargó correctamente
        if (typeof faceapi === 'undefined' || !faceapi.nets) {
            throw new Error('face-api.js no se cargó correctamente. Revisa tu conexión.');
        }

        console.log('face-api.js cargado correctamente, versión:', faceapi.version || 'desconocida');

        // Configurar backend de TensorFlow
        try {
            await faceapi.tf.setBackend('webgl');
            await faceapi.tf.ready();
            console.log('Usando backend WebGL');
        } catch (e) {
            console.warn('WebGL no disponible, intentando CPU...');
            await faceapi.tf.setBackend('cpu');
            await faceapi.tf.ready();
            console.log('Usando backend CPU');
        }

        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.14/model';

        statusEl.textContent = 'Descargando modelo de detección...';
        await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
        statusEl.textContent = 'Descargando modelo de expresiones...';
        await faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);

        statusEl.textContent = 'Modelos cargados. Iniciando cámara...';
        await startCamera();
    } catch (err) {
        console.error('Error al cargar modelos:', err);
        statusEl.textContent = 'Error al cargar IA. Revisa tu conexión.';
        statusEl.style.color = '#ff6b6b';
    }
}

async function startCamera() {
    const statusEl = document.getElementById('camera-status');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 320, height: 240, facingMode: 'user' }
        });

        video.srcObject = stream;
        await video.play();

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        statusEl.textContent = 'Cámara activa - Detectando emociones...';
        statusEl.style.color = '#8fefab';

        // Iniciar detección cada 500ms
        detectionInterval = setInterval(detectEmotion, 500);

    } catch (err) {
        console.error('Error de cámara:', err);
        statusEl.textContent = 'No se pudo acceder a la cámara';
        statusEl.style.color = '#ff6b6b';
    }
}

async function detectEmotion() {
    if (!video || video.paused || video.ended) return;

    try {
        const detection = await faceapi
            .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceExpressions();

        // Limpiar canvas
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (detection) {
            const expressions = detection.expressions;
            const sadness = expressions.sad || 0;
            const happiness = expressions.happy || 0;

            // Dibujar indicador de emoción
            drawEmotionIndicator(ctx, expressions);

            // === SONRISA → Cinnamonroll + brillo ===
            if (happiness > 0.5) {
                noSmileFrames = 0;
                smileFrames++;
                if (smileFrames >= SMILE_FRAMES_NEEDED && !isShowingCinnamonroll) {
                    showCinnamonroll();
                }
            } else {
                smileFrames = 0;
                if (isShowingCinnamonroll) {
                    noSmileFrames++;
                    if (noSmileFrames >= NO_SMILE_FRAMES_NEEDED) {
                        hideCinnamonroll();
                    }
                }
            }

            // === TRISTEZA → Video ===
            if (sadness > 0.5 && !isShowingVideo) {
                happyFrames = 0;
                if (!sadnessTimeout) {
                    sadnessTimeout = setTimeout(() => {
                        showVideoPopup();
                    }, 1500);
                }
            } else if (sadness <= 0.5) {
                // Si dejó de estar triste, cancelar timeout
                if (sadnessTimeout) {
                    clearTimeout(sadnessTimeout);
                    sadnessTimeout = null;
                }
                // Si el video está mostrándose, contar frames felices
                if (isShowingVideo) {
                    happyFrames++;
                    if (happyFrames >= HAPPY_FRAMES_NEEDED) {
                        closeVideoPopup();
                    }
                }
            }
        }
    } catch (err) {
        // Silenciar errores de detección intermitentes
    }
}

function drawEmotionIndicator(ctx, expressions) {
    const emotions = [
        { name: 'Feliz', value: expressions.happy, color: '#4ade80' },
        { name: 'Triste', value: expressions.sad, color: '#60a5fa' },
        { name: 'Neutral', value: expressions.neutral, color: '#a78bfa' }
    ];

    // Encontrar emoción dominante
    let dominant = emotions[0];
    emotions.forEach(e => {
        if (e.value > dominant.value) dominant = e;
    });

    // Mostrar emoción dominante
    ctx.font = '14px Georgia';
    ctx.fillStyle = dominant.color;
    ctx.textAlign = 'left';
    ctx.fillText(`${dominant.name}: ${Math.round(dominant.value * 100)}%`, 10, 20);

    // Barra de tristeza
    const barWidth = 100;
    const sadPercent = expressions.sad || 0;
    ctx.fillStyle = 'rgba(255,255,255,0.2)';
    ctx.fillRect(10, 28, barWidth, 6);
    ctx.fillStyle = sadPercent > 0.5 ? '#ff6b6b' : '#60a5fa';
    ctx.fillRect(10, 28, barWidth * sadPercent, 6);
}

function showCinnamonroll() {
    isShowingCinnamonroll = true;
    const cinna = document.getElementById('cinnamonroll');
    const glass = document.querySelector('.glass');
    if (cinna) {
        cinna.classList.remove('float', 'done');
        cinna.classList.add('show');
        // Dibujar Cinnamonroll usando Python/Brython
        if (typeof window.drawCinnamonrollPython === 'function') {
            window.drawCinnamonrollPython();
            // Cuando termine de dibujar, flotar y mostrar mensaje
            setTimeout(() => {
                cinna.classList.add('float', 'done');
            }, 100);
        }
    }
    if (glass) glass.classList.add('smile-glow');
}

function hideCinnamonroll() {
    isShowingCinnamonroll = false;
    noSmileFrames = 0;
    const cinna = document.getElementById('cinnamonroll');
    const glass = document.querySelector('.glass');
    if (cinna) {
        cinna.classList.remove('show', 'float', 'done');
        // Limpiar canvas usando Python/Brython
        if (typeof window.clearCinnamonrollPython === 'function') {
            setTimeout(() => window.clearCinnamonrollPython(), 600);
        }
    }
    if (glass) glass.classList.remove('smile-glow');
}

function showVideoPopup() {
    isShowingVideo = true;
    happyFrames = 0;

    const popup = document.getElementById('meme-popup');
    popup.classList.add('show');

    if (sadVideo) {
        sadVideo.currentTime = 0;
        sadVideo.play().catch(e => console.warn('No se pudo reproducir video:', e));
    }
}

function closeVideoPopup() {
    const popup = document.getElementById('meme-popup');
    popup.classList.remove('show');

    if (sadVideo) {
        sadVideo.pause();
        sadVideo.currentTime = 0;
    }

    isShowingVideo = false;
    happyFrames = 0;
    sadnessTimeout = null;
}

// Cerrar popup con Escape
document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isShowingVideo) {
            closeVideoPopup();
        }
    });

    // Iniciar la app
    init();
});

// ============================================
// BOTONES DE PRUEBA
// ============================================
function testHappy() {
    if (isShowingVideo) closeVideoPopup();
    if (!isShowingCinnamonroll) {
        showCinnamonroll();
    } else {
        hideCinnamonroll();
    }
}

function testSad() {
    if (isShowingCinnamonroll) hideCinnamonroll();
    if (!isShowingVideo) {
        showVideoPopup();
    } else {
        closeVideoPopup();
    }
}
