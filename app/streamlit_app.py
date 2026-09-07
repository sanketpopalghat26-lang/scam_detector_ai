"""Streamlit Web Application: Multi-Channel Cyber Scam Detection Dashboard.
Whitehat AI with interactive green net grid, smooth shooting star falling animation in hero box,
and aesthetic yellow/white typography.
"""

import sys
import os
import json
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# Configure page settings without emojis
st.set_page_config(
    page_title="Whitehat AI | Threat Intelligence & Scam Defense",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Interactive Green Net Grid + Smooth Hero Shooting Stars Canvas Engine
components.html("""
<script>
(function() {
    const parentDoc = window.parent.document;
    
    // -------------------------------------------------------------
    // 1. Full-Screen Interactive Net Grid Canvas
    // -------------------------------------------------------------
    let netCanvas = parentDoc.getElementById('cyber-net-canvas');
    if (!netCanvas) {
        netCanvas = parentDoc.createElement('canvas');
        netCanvas.id = 'cyber-net-canvas';
        netCanvas.style.position = 'fixed';
        netCanvas.style.top = '0';
        netCanvas.style.left = '0';
        netCanvas.style.width = '100vw';
        netCanvas.style.height = '100vh';
        netCanvas.style.zIndex = '0';
        netCanvas.style.pointerEvents = 'none';
        netCanvas.style.backgroundColor = '#04070d';
        parentDoc.body.prepend(netCanvas);
    }
    
    const netCtx = netCanvas.getContext('2d');
    let netWidth, netHeight;
    let gridPoints = [];
    const spacing = 48;
    
    const mouse = {
        x: -1000,
        y: -1000,
        radius: 200
    };
    
    function resizeNet() {
        netWidth = netCanvas.width = window.parent.innerWidth;
        netHeight = netCanvas.height = window.parent.innerHeight;
        initGrid();
    }
    
    function initGrid() {
        gridPoints = [];
        const cols = Math.ceil(netWidth / spacing) + 2;
        const rows = Math.ceil(netHeight / spacing) + 2;
        
        for (let r = 0; r < rows; r++) {
            gridPoints[r] = [];
            for (let c = 0; c < cols; c++) {
                const bx = (c - 1) * spacing;
                const by = (r - 1) * spacing;
                gridPoints[r][c] = {
                    baseX: bx,
                    baseY: by,
                    x: bx,
                    y: by,
                    vx: 0,
                    vy: 0,
                    phase: (c * 0.3) + (r * 0.3)
                };
            }
        }
    }
    
    function onMouseMove(e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    }
    
    function onTouchMove(e) {
        if (e.touches.length > 0) {
            mouse.x = e.touches[0].clientX;
            mouse.y = e.touches[0].clientY;
        }
    }
    
    parentDoc.addEventListener('mousemove', onMouseMove, { passive: true });
    parentDoc.addEventListener('touchmove', onTouchMove, { passive: true });
    window.addEventListener('resize', resizeNet);
    resizeNet();
    
    let netFrame = 0;
    function animateNet() {
        netFrame++;
        const time = netFrame * 0.025;
        
        netCtx.clearRect(0, 0, netWidth, netHeight);
        
        const bgGrad = netCtx.createRadialGradient(netWidth/2, netHeight/2, netWidth*0.1, netWidth/2, netHeight/2, netWidth*0.8);
        bgGrad.addColorStop(0, '#060c14');
        bgGrad.addColorStop(1, '#020408');
        netCtx.fillStyle = bgGrad;
        netCtx.fillRect(0, 0, netWidth, netHeight);
        
        const rows = gridPoints.length;
        if (rows > 0) {
            const cols = gridPoints[0].length;
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const p = gridPoints[r][c];
                    const waveX = Math.sin(time + p.phase) * 6;
                    const waveY = Math.cos(time + p.phase * 1.2) * 6;
                    
                    const dx = mouse.x - p.x;
                    const dy = mouse.y - p.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    let forceX = 0;
                    let forceY = 0;
                    if (dist < mouse.radius && dist > 0) {
                        const power = (1 - dist / mouse.radius);
                        const angle = Math.atan2(dy, dx);
                        const push = power * 45;
                        forceX = -Math.cos(angle) * push;
                        forceY = -Math.sin(angle) * push;
                    }
                    
                    const targetX = p.baseX + waveX + forceX;
                    const targetY = p.baseY + waveY + forceY;
                    
                    p.vx = (targetX - p.x) * 0.12;
                    p.vy = (targetY - p.y) * 0.12;
                    p.x += p.vx;
                    p.y += p.vy;
                }
            }
            
            netCtx.strokeStyle = 'rgba(16, 215, 120, 0.42)';
            netCtx.lineWidth = 1.35;
            netCtx.shadowColor = '#00ff88';
            netCtx.shadowBlur = 4;
            
            for (let r = 0; r < rows; r++) {
                netCtx.beginPath();
                netCtx.moveTo(gridPoints[r][0].x, gridPoints[r][0].y);
                for (let c = 1; c < cols - 1; c++) {
                    const xc = (gridPoints[r][c].x + gridPoints[r][c + 1].x) / 2;
                    const yc = (gridPoints[r][c].y + gridPoints[r][c + 1].y) / 2;
                    netCtx.quadraticCurveTo(gridPoints[r][c].x, gridPoints[r][c].y, xc, yc);
                }
                netCtx.lineTo(gridPoints[r][cols - 1].x, gridPoints[r][cols - 1].y);
                netCtx.stroke();
            }
            
            for (let c = 0; c < cols; c++) {
                netCtx.beginPath();
                netCtx.moveTo(gridPoints[0][c].x, gridPoints[0][c].y);
                for (let r = 1; r < rows - 1; r++) {
                    const xc = (gridPoints[r][c].x + gridPoints[r + 1][c].x) / 2;
                    const yc = (gridPoints[r][c].y + gridPoints[r + 1][c].y) / 2;
                    netCtx.quadraticCurveTo(gridPoints[r][c].x, gridPoints[r][c].y, xc, yc);
                }
                netCtx.lineTo(gridPoints[rows - 1][c].x, gridPoints[rows - 1][c].y);
                netCtx.stroke();
            }
        }
        
        if (mouse.x > 0 && mouse.y > 0) {
            const glow = netCtx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, mouse.radius * 1.2);
            glow.addColorStop(0, 'rgba(0, 255, 140, 0.12)');
            glow.addColorStop(1, 'rgba(0, 255, 140, 0)');
            netCtx.fillStyle = glow;
            netCtx.beginPath();
            netCtx.arc(mouse.x, mouse.y, mouse.radius * 1.2, 0, Math.PI * 2);
            netCtx.fill();
        }
        
        requestAnimationFrame(animateNet);
    }
    animateNet();

    // -------------------------------------------------------------
    // 2. Smooth Falling Shooting Stars in Hero Box
    // -------------------------------------------------------------
    let heroStars = [];
    let bgTwinkleStars = [];
    const NUM_SHOOTING_LANES = 6;
    
    function initHeroStars(w, h) {
        // Background subtle twinkling stars
        bgTwinkleStars = [];
        const numTwinkle = 35;
        const colors = ['#ffffff', '#fef08a', '#38bdf8', '#f472b6', '#e0e7ff'];
        for (let i = 0; i < numTwinkle; i++) {
            bgTwinkleStars.push({
                x: Math.random() * w,
                y: Math.random() * h,
                radius: 0.8 + Math.random() * 1.6,
                color: colors[Math.floor(Math.random() * colors.length)],
                phase: Math.random() * Math.PI * 2,
                speed: 0.02 + Math.random() * 0.03,
                sparkle: Math.random() > 0.65
            });
        }
        
        // Shooting stars assigned to non-overlapping diagonal lanes
        heroStars = [];
        const laneWidth = w / NUM_SHOOTING_LANES;
        for (let i = 0; i < NUM_SHOOTING_LANES; i++) {
            heroStars.push({
                lane: i,
                x: i * laneWidth + Math.random() * (laneWidth * 0.7),
                y: -100 - (i * 120 + Math.random() * 100),
                length: 90 + Math.random() * 60,
                speed: 7.5 + Math.random() * 4,
                angle: Math.PI / 4, // 45 degrees diagonal trajectory
                active: false,
                delay: i * 45 + Math.floor(Math.random() * 40),
                headColor: Math.random() > 0.3 ? '#ffffff' : '#fef08a',
                tailColor: Math.random() > 0.4 ? 'rgba(56, 189, 248, ' : 'rgba(254, 240, 138, '
            });
        }
    }
    
    function drawStarFlare(ctx, cx, cy, radius, color) {
        ctx.save();
        ctx.fillStyle = color;
        ctx.shadowColor = color;
        ctx.shadowBlur = 8;
        
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        ctx.fill();
        
        // 4-point light ray burst
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        const rayLen = radius * 3.5;
        
        ctx.beginPath();
        ctx.moveTo(cx - rayLen, cy);
        ctx.lineTo(cx + rayLen, cy);
        ctx.moveTo(cx, cy - rayLen);
        ctx.lineTo(cx, cy + rayLen);
        ctx.stroke();
        
        ctx.restore();
    }
    
    let lastHeroW = 0, lastHeroH = 0;
    function animateHeroStars() {
        const heroCanvas = parentDoc.getElementById('hero-stars-canvas');
        if (heroCanvas) {
            const rect = heroCanvas.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                if (heroCanvas.width !== Math.floor(rect.width) || heroCanvas.height !== Math.floor(rect.height)) {
                    heroCanvas.width = Math.floor(rect.width);
                    heroCanvas.height = Math.floor(rect.height);
                    lastHeroW = heroCanvas.width;
                    lastHeroH = heroCanvas.height;
                    initHeroStars(lastHeroW, lastHeroH);
                }
                
                const hCtx = heroCanvas.getContext('2d');
                const w = heroCanvas.width;
                const h = heroCanvas.height;
                
                hCtx.clearRect(0, 0, w, h);
                
                // 1. Draw twinkling cosmos stars
                for (let i = 0; i < bgTwinkleStars.length; i++) {
                    const s = bgTwinkleStars[i];
                    s.phase += s.speed;
                    const alpha = 0.3 + 0.6 * (0.5 + 0.5 * Math.sin(s.phase));
                    
                    hCtx.save();
                    hCtx.globalAlpha = alpha;
                    if (s.sparkle && alpha > 0.7) {
                        drawStarFlare(hCtx, s.x, s.y, s.radius * 1.2, s.color);
                    } else {
                        hCtx.fillStyle = s.color;
                        hCtx.beginPath();
                        hCtx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                        hCtx.fill();
                    }
                    hCtx.restore();
                }
                
                // 2. Draw smoothly falling shooting stars (without collision/overlapping)
                const laneWidth = w / NUM_SHOOTING_LANES;
                for (let i = 0; i < heroStars.length; i++) {
                    const star = heroStars[i];
                    
                    if (star.delay > 0) {
                        star.delay--;
                        continue;
                    }
                    
                    const dx = Math.cos(star.angle);
                    const dy = Math.sin(star.angle);
                    
                    star.x += dx * star.speed;
                    star.y += dy * star.speed;
                    
                    const tailX = star.x - dx * star.length;
                    const tailY = star.y - dy * star.length;
                    
                    // Draw smooth gradient tail
                    const grad = hCtx.createLinearGradient(tailX, tailY, star.x, star.y);
                    grad.addColorStop(0, star.tailColor + '0)');
                    grad.addColorStop(0.65, star.tailColor + '0.45)');
                    grad.addColorStop(1, 'rgba(255, 255, 255, 0.95)');
                    
                    hCtx.save();
                    hCtx.strokeStyle = grad;
                    hCtx.lineWidth = 1.8;
                    hCtx.lineCap = 'round';
                    hCtx.shadowColor = '#ffffff';
                    hCtx.shadowBlur = 6;
                    
                    hCtx.beginPath();
                    hCtx.moveTo(tailX, tailY);
                    hCtx.lineTo(star.x, star.y);
                    hCtx.stroke();
                    
                    // Glowing shooting star head
                    drawStarFlare(hCtx, star.x, star.y, 2.2, star.headColor);
                    hCtx.restore();
                    
                    // Respawn star smoothly when it exits canvas
                    if (tailY > h + 50 || tailX > w + 50) {
                        star.x = star.lane * laneWidth + Math.random() * (laneWidth * 0.7) - 60;
                        star.y = -60 - Math.random() * 80;
                        star.length = 90 + Math.random() * 60;
                        star.speed = 7.5 + Math.random() * 4;
                        star.delay = 35 + Math.floor(Math.random() * 70); // Staggered delay ensures no overlap
                    }
                }
            }
        }
        requestAnimationFrame(animateHeroStars);
    }
    animateHeroStars();

    // -------------------------------------------------------------
    // 3. Navigation Links -> Streamlit Tab Switching
    // -------------------------------------------------------------
    function hookNavTabs() {
        const navLinks = parentDoc.querySelectorAll('.nav-links a');
        if (!navLinks || navLinks.length === 0) return;
        
        navLinks.forEach((link, idx) => {
            if (link.dataset.hooked) return;
            link.dataset.hooked = "true";
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const tabs = parentDoc.querySelectorAll('.stTabs [data-baseweb="tab"]');
                if (tabs && tabs[idx]) {
                    tabs[idx].click();
                    const det = parentDoc.getElementById('detection');
                    if (det) {
                        det.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        });
    }
    setInterval(hookNavTabs, 600);
})();
</script>
""", height=0)

# Custom CSS for Yellow & White Luxury Theme over Net Grid & Shooting Stars
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500;1,6..72,600&display=swap');

    /* Global canvas & translucent background */
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    a {
        text-decoration: none !important;
    }

    #MainMenu, header, footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
        position: relative;
        z-index: 1;
    }

    /* Top Navigation Bar */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1.75rem;
        background: rgba(10, 16, 26, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(250, 204, 21, 0.2);
        border-radius: 9999px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #ffffff !important;
    }
    .brand-badge-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #facc15;
        box-shadow: 0 0 10px #facc15;
        display: inline-block;
    }
    .nav-links {
        display: flex;
        gap: 2.2rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    .nav-links a {
        color: #cbd5e1 !important;
        font-size: 0.92rem;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .nav-links a:hover {
        color: #facc15 !important;
    }

    /* Hero Section with Glass Arch & Shooting Stars Canvas */
    .hero-wrapper {
        position: relative;
        text-align: center;
        padding: 3.5rem 1.5rem;
        background: radial-gradient(ellipse 850px 450px at 50% 35%, rgba(12, 22, 42, 0.85) 0%, rgba(8, 14, 28, 0.75) 60%, rgba(4, 8, 18, 0.65) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(250, 204, 21, 0.25);
        border-radius: 36px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        overflow: hidden;
    }

    .hero-stars-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    /* Floating badges arch */
    .arch-badges {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    .floating-app-icon {
        background: rgba(15, 25, 40, 0.88);
        width: 56px;
        height: 56px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .floating-app-icon:hover {
        transform: translateY(-4px);
        border-color: #facc15;
    }
    .icon-1 { transform: translateY(14px) rotate(-4deg); }
    .icon-2 { transform: translateY(3px) rotate(-2deg); }
    .icon-3 { transform: translateY(-6px); }
    .icon-4 { transform: translateY(3px) rotate(2deg); }
    .icon-5 { transform: translateY(14px) rotate(4deg); }

    /* Hero Headline - Yellow & White Combination with Tilted Aesthetic Word */
    h1.hero-headline, .hero-headline {
        font-family: 'Newsreader', 'Playfair Display', Georgia, serif !important;
        font-size: 4.1rem !important;
        line-height: 1.12 !important;
        font-weight: 400 !important;
        letter-spacing: -0.025em !important;
        color: #ffffff !important;
        margin: 0 auto 1.35rem auto !important;
        max-width: 860px !important;
    }

    .tilted-yellow-word {
        font-family: 'Newsreader', 'Playfair Display', Georgia, serif !important;
        font-style: italic !important;
        color: #facc15 !important;
        display: inline-block;
        transform: rotate(-3.5deg);
        margin: 0 0.12em;
        text-shadow: 0 0 25px rgba(250, 204, 21, 0.45);
        font-weight: 500 !important;
    }

    .hero-subheadline {
        font-size: 1.1rem;
        line-height: 1.65;
        color: #cbd5e1;
        max-width: 660px;
        margin: 0 auto;
        font-weight: 400;
    }

    /* Clean Frosted Cards */
    .clean-card {
        background: rgba(10, 18, 30, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 1.75rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.5rem;
    }

    .card-title {
        font-family: 'Newsreader', serif;
        font-size: 1.55rem;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 0.35rem;
    }
    .card-description {
        font-size: 0.92rem;
        color: #94a3b8;
        margin-bottom: 1.25rem;
    }

    /* Verdict Badges */
    .verdict-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem 1.15rem;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-bottom: 1rem;
    }
    .verdict-scam {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .verdict-benign {
        background-color: rgba(250, 204, 21, 0.15);
        color: #facc15;
        border: 1px solid rgba(250, 204, 21, 0.4);
    }

    /* Factor List */
    .factor-pill {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 0.88rem;
    }
    .factor-risk {
        border-left: 3px solid #ef4444;
    }
    .factor-safe {
        border-left: 3px solid #facc15;
    }

    /* Premium Rotating RGB Conic Animation */
    @property --angle {
        syntax: '<angle>';
        initial-value: 0deg;
        inherits: false;
    }

    @keyframes rotateRGB {
        0% {
            --angle: 0deg;
        }
        100% {
            --angle: 360deg;
        }
    }

    /* Animated Rotating RGB Border on Text Inputs and Text Areas */
    .stTextInput > div, .stTextArea > div {
        position: relative !important;
        border-radius: 16px !important;
        padding: 2px !important;
        background: conic-gradient(from var(--angle, 0deg), #ff0055, #ff5500, #ffea00, #00ff66, #00e1ff, #7a00ff, #ff0055) !important;
        animation: rotateRGB 3.5s linear infinite !important;
        box-shadow: 0 0 16px rgba(0, 225, 255, 0.25), 0 0 35px rgba(255, 0, 85, 0.15) !important;
        transition: box-shadow 0.3s ease !important;
        border: none !important;
    }

    .stTextInput > div:focus-within, .stTextArea > div:focus-within {
        box-shadow: 0 0 25px rgba(0, 225, 255, 0.55), 0 0 50px rgba(255, 0, 85, 0.35) !important;
    }

    .stTextInput [data-baseweb="input"], .stTextArea [data-baseweb="textarea"] {
        border: none !important;
        background-color: transparent !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }

    .stTextInput input, .stTextArea textarea {
        border-radius: 14px !important;
        border: none !important;
        background-color: #080e18 !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        box-shadow: none !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        background-color: #0a111e !important;
        color: #ffffff !important;
        outline: none !important;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #facc15 0%, #eab308 100%) !important;
        color: #0f172a !important;
        border-radius: 9999px !important;
        padding: 0.6rem 1.6rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 18px rgba(250, 204, 21, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #fde047 0%, #facc15 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 22px rgba(250, 204, 21, 0.45) !important;
    }
    .stButton button[kind="secondary"] {
        border-radius: 9999px !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #cbd5e1 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    .stButton button[kind="secondary"]:hover {
        border-color: #facc15 !important;
        color: #facc15 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(10, 16, 26, 0.75);
        backdrop-filter: blur(12px);
        padding: 6px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        justify-content: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px !important;
        padding: 8px 22px !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        color: #94a3b8 !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(250, 204, 21, 0.15) !important;
        color: #facc15 !important;
        border: 1px solid rgba(250, 204, 21, 0.4) !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Load model predictor
try:
    from src.predict import ScamPredictor
    from src.features.url_features import extract_domain_parts
    from src.features.text_features import URL_REGEX
    from src.ingestion.synthetic_data import (
        generate_benchmark_sms,
        generate_benchmark_emails,
        generate_benchmark_urls
    )
    predictor = ScamPredictor()
except Exception as e:
    predictor = None

# -------------------------------------------------------------
# 1. Top Navigation Bar
# -------------------------------------------------------------
st.markdown("""<div class="nav-container">
<a href="#" class="brand-logo"><span class="brand-badge-dot"></span> Whitehat AI</a>
<ul class="nav-links">
<li><a href="#detection">SMS Scanner</a></li>
<li><a href="#detection">Email Phishing</a></li>
<li><a href="#detection">URL Inspector</a></li>
<li><a href="#detection">Compound Fusion</a></li>
<li><a href="#detection">Benchmarks</a></li>
</ul>
</div>""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Hero Section with Shooting Stars Canvas
# -------------------------------------------------------------
st.markdown("""<div class="hero-wrapper">
<canvas id="hero-stars-canvas" class="hero-stars-canvas"></canvas>
<div class="hero-content">
<div class="arch-badges">
<div class="floating-app-icon icon-1">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
<path d="M6 12C6 15.3137 8.68629 18 12 18C15.3137 18 18 15.3137 18 12C18 8.68629 15.3137 6 12 6C8.68629 6 6 8.68629 6 12Z" fill="#38bdf8"/>
<path d="M4 8C4 5.79086 5.79086 4 8 4H16C18.2091 4 20 5.79086 20 8V16C20 18.2091 18.2091 20 16 20H8C5.79086 20 4 18.2091 4 16V8Z" stroke="#38bdf8" stroke-width="2"/>
</svg>
</div>
<div class="floating-app-icon icon-2">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
</svg>
</div>
<div class="floating-app-icon icon-3">
<svg width="26" height="26" viewBox="0 0 24 24" fill="none">
<rect x="3" y="5" width="18" height="14" rx="3" stroke="#facc15" stroke-width="2"/>
<path d="M3 8L12 13L21 8" stroke="#facc15" stroke-width="2" stroke-linecap="round"/>
</svg>
</div>
<div class="floating-app-icon icon-4">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
<circle cx="12" cy="12" r="10" stroke="#fb923c" stroke-width="2"/>
<circle cx="9" cy="10" r="1.5" fill="#fb923c"/>
<circle cx="15" cy="10" r="1.5" fill="#fb923c"/>
<path d="M8 15C9.5 16.5 14.5 16.5 16 15" stroke="#fb923c" stroke-width="1.8" stroke-linecap="round"/>
</svg>
</div>
<div class="floating-app-icon icon-5">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
<path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z" fill="#38bdf8"/>
</svg>
</div>
</div>
<h1 class="hero-headline">Your Haven for<br><span class="tilted-yellow-word">Seamless</span> AI Fraud Defense</h1>
<p class="hero-subheadline">
Empowering you with intelligent, effortless tools to streamline your security workflow, eliminate cyber scams, and protect digital communications—seamlessly.
</p>
</div>
</div>""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. Interactive Threat Inspection Suite
# -------------------------------------------------------------
st.markdown('<div id="detection"></div>', unsafe_allow_html=True)

tab_sms, tab_email, tab_url, tab_incident, tab_metrics = st.tabs([
    "SMS Intelligence",
    "Email Phishing",
    "URL Inspector",
    "Compound Incident",
    "Model Benchmark"
])

# ----------------- TAB 1: SMS -----------------
with tab_sms:
    col_l, col_r = st.columns([1.1, 0.9], gap="large")
    with col_l:
        st.markdown('<div class="card-title">SMS Smishing Detection</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-description">Inspect SMS messages for deceptive bank notifications, credential theft, and payment scams.</div>', unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom: 6px;'>Quick Test Presets:</p>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        sms_val = ""
        if b1.button("Urgent Bank Alert", key="s_btn1", use_container_width=True):
            sms_val = "URGENT: Your Chase account has been temporarily locked due to unusual debit activity. Unlock now at http://secure-chase-update.xyz"
        if b2.button("Legitimate SMS", key="s_btn2", use_container_width=True):
            sms_val = "Hey Sarah, confirming our lunch meeting tomorrow at 12:30 PM. See you then!"
            
        sms_text = st.text_area("Message Content", value=sms_val, height=130, placeholder="Paste or type SMS text here...")
        run_sms = st.button("Inspect SMS Threat", type="primary", use_container_width=True, key="run_sms_act")

    with col_r:
        if (run_sms or sms_text) and sms_text.strip() and predictor:
            with st.spinner("Analyzing message vectors..."):
                res = predictor.predict_sms(sms_text)
            
            is_scam = res["verdict"] == "SCAM"
            badge_class = "verdict-scam" if is_scam else "verdict-benign"
            badge_icon = "Threat Flagged" if is_scam else "Verified Safe"
            
            st.markdown(f'<div class="verdict-badge {badge_class}">{badge_icon} — {res["verdict"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**Calibrated Risk Probability:** `{res['risk_score_pct']}%` ({res['risk_level']})")
            st.progress(float(res["confidence"]))

            st.markdown("<p style='font-weight:600; font-size:0.9rem; margin-top:1.2rem; color:#facc15;'>Key Explainability Signals:</p>", unsafe_allow_html=True)
            for f in res.get("top_factors", []):
                pill_type = "factor-risk" if f["direction"] == "Risk Escalator" else "factor-safe"
                st.markdown(f'''
                <div class="factor-pill {pill_type}">
                    <span>{f["feature"]}</span>
                    <span style="font-weight:600; color:{'#f87171' if f['direction']=='Risk Escalator' else '#facc15'};">{f["impact"]:+.3f}</span>
                </div>
                ''', unsafe_allow_html=True)

            if res.get("embedded_urls_analysis"):
                st.markdown("<p style='font-weight:600; font-size:0.9rem; margin-top:1rem;'>Embedded Link Breakdown:</p>", unsafe_allow_html=True)
                for u in res["embedded_urls_analysis"]:
                    tag = "Scam Link" if u["verdict"] == "SCAM" else "Benign Link"
                    st.caption(f"• **{u['url']}** → {tag} ({u['risk_score_pct']}%)")
        else:
            st.markdown("""
            <div style="background:rgba(15, 23, 42, 0.4); border:1px dashed rgba(255, 255, 255, 0.15); border-radius:16px; padding:3rem 1.5rem; text-align:center; color:#94a3b8;">
                <p style="margin:0; font-size:0.95rem;">Enter message text or pick a preset sample on the left to view threat analysis.</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 2: Email -----------------
with tab_email:
    col_l, col_r = st.columns([1.1, 0.9], gap="large")
    with col_l:
        st.markdown('<div class="card-title">Email Phishing & BEC Scanner</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-description">Evaluate email subjects and body text for brand spoofing, urgency heuristics, and credential harvesting.</div>', unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom: 6px;'>Quick Test Presets:</p>", unsafe_allow_html=True)
        e1, e2 = st.columns(2)
        email_val = ""
        if e1.button("PayPal Phishing Alert", key="e_btn1", use_container_width=True):
            email_val = "Subject: URGENT: Unauthorized PayPal Access Detected\n\nDear Client,\nWe noticed unusual transactions on your account. To prevent immediate permanent suspension, please verify your identity at http://paypa1-security-login.xyz/auth/verify\n\nPayPal Security Team"
        if e2.button("Internal Team Email", key="e_btn2", use_container_width=True):
            email_val = "Subject: Sprint Planning Agenda - Q3 Deliverables\n\nHi Team,\nPlease find attached our agenda for this Thursday's planning session. Let me know if you want to add any talking points.\n\nBest,\nMarcus"
            
        email_text = st.text_area("Email Content", value=email_val, height=150, placeholder="Subject: ...\n\nBody...")
        run_email = st.button("Inspect Email Threat", type="primary", use_container_width=True, key="run_email_act")

    with col_r:
        if (run_email or email_text) and email_text.strip() and predictor:
            with st.spinner("Evaluating email semantics..."):
                res = predictor.predict_email(email_text)
            
            is_scam = res["verdict"] == "SCAM"
            badge_class = "verdict-scam" if is_scam else "verdict-benign"
            badge_icon = "Phishing Flagged" if is_scam else "Legitimate Email"
            
            st.markdown(f'<div class="verdict-badge {badge_class}">{badge_icon} — {res["verdict"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**Phishing Risk Score:** `{res['risk_score_pct']}%` ({res['risk_level']})")
            st.progress(float(res["confidence"]))

            st.markdown("<p style='font-weight:600; font-size:0.9rem; margin-top:1.2rem; color:#facc15;'>Feature Attribution Factors:</p>", unsafe_allow_html=True)
            for f in res.get("top_factors", []):
                pill_type = "factor-risk" if f["direction"] == "Risk Escalator" else "factor-safe"
                st.markdown(f'''
                <div class="factor-pill {pill_type}">
                    <span>{f["feature"]}</span>
                    <span style="font-weight:600; color:{'#f87171' if f['direction']=='Risk Escalator' else '#facc15'};">{f["impact"]:+.3f}</span>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(15, 23, 42, 0.4); border:1px dashed rgba(255, 255, 255, 0.15); border-radius:16px; padding:3rem 1.5rem; text-align:center; color:#94a3b8;">
                <p style="margin:0; font-size:0.95rem;">Enter email text or select a preset sample to view real-time classification.</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 3: URL -----------------
with tab_url:
    col_l, col_r = st.columns([1.1, 0.9], gap="large")
    with col_l:
        st.markdown('<div class="card-title">Malicious URL & Typosquatting Engine</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-description">Extract structural tokens, Levenshtein distance against global brands, deceptive subdomains, and suspicious TLDs.</div>', unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom: 6px;'>Quick Test Presets:</p>", unsafe_allow_html=True)
        u1, u2, u3 = st.columns(3)
        url_val = ""
        if u1.button("Brand Typosquat", key="u_btn1", use_container_width=True):
            url_val = "http://paypa1-security-login.xyz/auth/verify"
        if u2.button("IP Address Host", key="u_btn2", use_container_width=True):
            url_val = "http://192.168.1.105:8080/admin/login.php"
        if u3.button("Legitimate Domain", key="u_btn3", use_container_width=True):
            url_val = "https://www.paypal.com/signin"
            
        url_text = st.text_input("Target URL", value=url_val, placeholder="https://example.com/login")
        run_url = st.button("Inspect Target URL", type="primary", use_container_width=True, key="run_url_act")

        if url_text.strip():
            d_info = extract_domain_parts(url_text)
            st.markdown("<p style='font-weight:600; font-size:0.85rem; margin-top:1rem; color:#94a3b8;'>Host Breakdown:</p>", unsafe_allow_html=True)
            st.json({
                "Host": d_info["host"],
                "Base Domain": d_info["base_domain"],
                "TLD": d_info["tld"],
                "Subdomains": d_info["subdomains"],
                "HTTPS Encrypted": d_info["is_https"],
                "Non-Standard Port": d_info["has_port"]
            })

    with col_r:
        if (run_url or url_text) and url_text.strip() and predictor:
            with st.spinner("Analyzing lexical structures & brand distances..."):
                res = predictor.predict_url(url_text)
            
            is_scam = res["verdict"] == "SCAM"
            badge_class = "verdict-scam" if is_scam else "verdict-benign"
            badge_icon = "Weaponized Domain" if is_scam else "Clean URL"
            
            st.markdown(f'<div class="verdict-badge {badge_class}">{badge_icon} — {res["verdict"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**URL Threat Score:** `{res['risk_score_pct']}%` ({res['risk_level']})")
            st.progress(float(res["confidence"]))

            st.markdown("<p style='font-weight:600; font-size:0.9rem; margin-top:1.2rem; color:#facc15;'>Top Contributing Risk Factors:</p>", unsafe_allow_html=True)
            for f in res.get("top_factors", []):
                pill_type = "factor-risk" if f["direction"] == "Risk Escalator" else "factor-safe"
                st.markdown(f'''
                <div class="factor-pill {pill_type}">
                    <span>{f["feature"]}</span>
                    <span style="font-weight:600; color:{'#f87171' if f['direction']=='Risk Escalator' else '#facc15'};">{f["impact"]:+.3f}</span>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(15, 23, 42, 0.4); border:1px dashed rgba(255, 255, 255, 0.15); border-radius:16px; padding:3rem 1.5rem; text-align:center; color:#94a3b8;">
                <p style="margin:0; font-size:0.95rem;">Enter a URL or pick a sample to view structural security analysis.</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 4: Compound Incident -----------------
with tab_incident:
    st.markdown('<div class="card-title">Multi-Channel Compound Incident Fusion</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-description">Ensemble cross-modality signals across text messages and embedded links with the Stacking Meta-Classifier.</div>', unsafe_allow_html=True)
    
    # Session state initialization for presets
    if "inc_preset_text" not in st.session_state:
        st.session_state.inc_preset_text = ""
    if "inc_preset_url" not in st.session_state:
        st.session_state.inc_preset_url = ""
    if "inc_preset_mod" not in st.session_state:
        st.session_state.inc_preset_mod = "Auto-Detect & Auto-Extract"

    st.markdown("<p style='font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom: 6px;'>Quick Test Compound Presets:</p>", unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns(3)
    if cp1.button("Credential Phish + URL", key="cp_btn1", use_container_width=True):
        st.session_state.inc_preset_text = "Subject: Immediate Security Update Required\n\nDear Chase Member,\nSuspicious debit activity was detected on your account. Your online banking will be suspended within 24 hours unless verified."
        st.session_state.inc_preset_url = "http://secure-chase-update.xyz/auth/login"
        st.session_state.inc_preset_mod = "Email Phishing + Target URL"
        st.rerun()

    if cp2.button("Smishing + Fake Domain", key="cp_btn2", use_container_width=True):
        st.session_state.inc_preset_text = "URGENT from PayPal: Unauthorized charge of $849.00 to CryptoExchange. If this wasn't you, dispute immediately at http://paypa1-security-login.xyz/auth/verify"
        st.session_state.inc_preset_url = "http://paypa1-security-login.xyz/auth/verify"
        st.session_state.inc_preset_mod = "SMS Smishing + Target URL"
        st.rerun()

    if cp3.button("Legitimate Multi-Channel Notice", key="cp_btn3", use_container_width=True):
        st.session_state.inc_preset_text = "Subject: Team Sync Agenda - Tomorrow at 10 AM\n\nHi everyone,\nPlease review the shared presentation slides before our sync meeting: https://docs.google.com/presentation\n\nBest,\nSecurity Operations"
        st.session_state.inc_preset_url = "https://docs.google.com/presentation"
        st.session_state.inc_preset_mod = "Email Phishing + Target URL"
        st.rerun()

    col_a, col_b = st.columns([1.1, 0.9], gap="large")
    with col_a:
        modality_options = ["Auto-Detect & Auto-Extract", "Email Phishing + Target URL", "SMS Smishing + Target URL"]
        def_idx = modality_options.index(st.session_state.inc_preset_mod) if st.session_state.inc_preset_mod in modality_options else 0
        inc_modality = st.radio("Modality Channel Configuration", modality_options, index=def_idx, horizontal=True)

        inc_body = st.text_area(
            "Incident Message Text",
            value=st.session_state.inc_preset_text,
            height=130,
            placeholder="Paste email body or SMS text message..."
        )
        inc_url_input = st.text_input(
            "Associated Target URL (Optional - will auto-extract from text if blank)",
            value=st.session_state.inc_preset_url,
            placeholder="https://suspicious-site.xyz/auth/verify"
        )
        run_inc = st.button("Evaluate Multi-Channel Incident", type="primary", use_container_width=True, key="run_inc_act")

    with col_b:
        should_run = (run_inc or inc_body.strip() or inc_url_input.strip()) and (inc_body.strip() or inc_url_input.strip()) and predictor
        if should_run:
            with st.spinner("Synthesizing multi-vector features with Stacking Meta-Classifier..."):
                # Determine email vs SMS based on modality
                target_email = None
                target_sms = None
                if inc_modality == "SMS Smishing + Target URL":
                    target_sms = inc_body.strip() if inc_body.strip() else None
                elif inc_modality == "Email Phishing + Target URL":
                    target_email = inc_body.strip() if inc_body.strip() else None
                else: # Auto-detect
                    if "Subject:" in inc_body or len(inc_body) > 180:
                        target_email = inc_body.strip() if inc_body.strip() else None
                    else:
                        target_sms = inc_body.strip() if inc_body.strip() else None

                target_url = inc_url_input.strip() if inc_url_input.strip() else None
                inc_res = predictor.predict_incident(
                    email_text=target_email,
                    sms_text=target_sms,
                    url=target_url
                )

            is_scam = inc_res["overall_verdict"] == "SCAM"
            badge_class = "verdict-scam" if is_scam else "verdict-benign"
            badge_icon = "Threat Confirmed" if is_scam else "Verified Safe"

            st.markdown(f'<div class="verdict-badge {badge_class}">{badge_icon} — {inc_res["overall_verdict"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**Unified Ensemble Risk:** `{inc_res['overall_risk_score_pct']}%` ({inc_res['overall_risk_level']})")
            st.progress(float(inc_res["overall_confidence"]))

            # Meta-Classifier Details Card
            meta = inc_res.get("ensemble_metadata", {})
            applied_weights = meta.get("applied_weights", {})
            weights_str = " • ".join([f"<b>{k.upper()}</b>: {w*100:.0f}%" for k, w in applied_weights.items()]) if applied_weights else "Equal weighted fusion"
            st.markdown(f"""
            <div style="background:rgba(15, 23, 42, 0.55); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:10px 14px; margin: 10px 0;">
                <span style="font-size:0.8rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em; font-family:'Fira Code',monospace;">Stacking Meta-Layer:</span>
                <div style="font-size:0.85rem; color:#facc15; margin-top:3px;">{meta.get('method', 'weighted_average').replace('_', ' ').title()} ({weights_str})</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<p style='font-weight:600; font-size:0.9rem; margin-top:1rem; color:#facc15;'>Contributing Modality Channels:</p>", unsafe_allow_html=True)
            for b_name, b_data in inc_res.get("branches", {}).items():
                b_scam = b_data['verdict'] == "SCAM"
                b_color = "#f87171" if b_scam else "#4ade80"
                st.markdown(f'''
                <div class="factor-pill" style="border-left: 3px solid {b_color};">
                    <span style="font-weight:600; text-transform:uppercase; color:#38bdf8;">{b_name} Channel</span>
                    <span style="font-weight:600; color:{b_color};">{b_data['verdict']} ({b_data['risk_score_pct']}%)</span>
                </div>
                ''', unsafe_allow_html=True)

                # Show top 2 factor explainabilities for each active branch
                factors = b_data.get("top_factors", [])[:2]
                for f in factors:
                    p_type = "factor-risk" if f.get("direction") == "Risk Escalator" else "factor-safe"
                    f_val = f.get('impact', 0)
                    st.markdown(f'''
                    <div class="factor-pill {p_type}" style="margin-left:14px; padding:0.45rem 0.8rem; font-size:0.82rem;">
                        <span>{f.get("feature", "Signal")}</span>
                        <span style="font-weight:600;">{f_val:+.2f}</span>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(15, 23, 42, 0.4); border:1px dashed rgba(255, 255, 255, 0.15); border-radius:16px; padding:3rem 1.5rem; text-align:center; color:#94a3b8;">
                <p style="margin:0; font-size:0.95rem;">Select a preset above or provide incident text and an associated target URL to execute multi-channel compound assessment.</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 5: Metrics & Architecture -----------------
with tab_metrics:
    st.markdown('<div class="card-title">Production Metrics & Validation Benchmark</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-description">Zero-leakage GroupShuffleSplit evaluation with cost-sensitive threshold calibration and live benchmark runner.</div>', unsafe_allow_html=True)
    
    # 1. Historical Production Benchmark Model Table
    metrics_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models_artifacts", "training_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics_data = json.load(f)
        
        rows = []
        for branch_key, data in metrics_data.items():
            if isinstance(data, dict) and "precision" in data:
                rows.append({
                    "Modality Branch": data.get("model_name", branch_key).upper(),
                    "Precision": f"{data.get('precision', 0)*100:.2f}%",
                    "Recall": f"{data.get('recall', 0)*100:.2f}%",
                    "F1-Score": f"{data.get('f1', 0):.4f}",
                    "ROC-AUC": f"{data.get('roc_auc', 0):.4f}" if data.get('roc_auc') else "N/A",
                    "False Negatives": data.get("false_negatives", 0)
                })
        if rows:
            th_style = "padding:10px 14px; text-align:left; border-bottom:1px solid rgba(255,255,255,0.15); color:#facc15; font-family:'Fira Code', monospace; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.05em;"
            td_style = "padding:10px 14px; border-bottom:1px solid rgba(255,255,255,0.06); color:#e2e8f0; font-size:0.9rem;"
            table_html = f"""
            <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.1); border-radius:12px; overflow:hidden; margin-bottom:1.5rem;">
                <table style="width:100%; border-collapse:collapse;">
                    <thead>
                        <tr style="background:rgba(255,255,255,0.03);">
                            <th style="{th_style}">Modality Branch</th>
                            <th style="{th_style}">Precision</th>
                            <th style="{th_style}">Recall</th>
                            <th style="{th_style}">F1-Score</th>
                            <th style="{th_style}">ROC-AUC</th>
                            <th style="{th_style}">False Negatives</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for r in rows:
                table_html += f"""
                        <tr>
                            <td style="{td_style} font-weight:600; color:#38bdf8;">{r['Modality Branch']}</td>
                            <td style="{td_style}">{r['Precision']}</td>
                            <td style="{td_style} font-weight:600; color:#4ade80;">{r['Recall']}</td>
                            <td style="{td_style}">{r['F1-Score']}</td>
                            <td style="{td_style}">{r['ROC-AUC']}</td>
                            <td style="{td_style} color:{'#f87171' if r['False Negatives'] > 0 else '#4ade80'};">{r['False Negatives']}</td>
                        </tr>
                """
            table_html += """
                    </tbody>
                </table>
            </div>
            """
            st.markdown(table_html, unsafe_allow_html=True)

    # 2. Interactive Live Benchmark Suite
    st.markdown('<div class="card-title" style="font-size:1.25rem; margin-top:1.5rem;">Interactive Live Benchmark Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-description">Benchmark real-time inference latency and classification accuracy against curated benchmark corpora.</div>', unsafe_allow_html=True)

    b_col1, b_col2, b_col3 = st.columns([1.5, 1, 1])
    with b_col1:
        bench_channel = st.selectbox("Benchmark Target Modality", ["All Branches (SMS + Email + URL)", "SMS Smishing", "Email Phishing", "URL Domain Inspector"], key="b_channel")
    with b_col2:
        bench_samples = st.selectbox("Sample Volume", [30, 60, 100], index=0, key="b_samples")
    with b_col3:
        st.write("")
        st.write("")
        run_benchmark_btn = st.button("Execute Live Benchmark", type="primary", use_container_width=True, key="run_benchmark_act")

    if run_benchmark_btn and predictor:
        with st.spinner(f"Evaluating {bench_samples} benchmark vectors across {bench_channel}..."):
            total_samples = 0
            correct = 0
            tp = 0
            fp = 0
            fn = 0
            tn = 0
            t_start = time.time()

            # Run benchmark on selected branches
            tasks = []
            if bench_channel in ["All Branches (SMS + Email + URL)", "SMS Smishing"]:
                n_branch = bench_samples if bench_channel != "All Branches (SMS + Email + URL)" else bench_samples // 3
                df_sms = generate_benchmark_sms(n_branch)
                for _, r in df_sms.iterrows():
                    tasks.append(("sms", r["text"], r["label"]))

            if bench_channel in ["All Branches (SMS + Email + URL)", "Email Phishing"]:
                n_branch = bench_samples if bench_channel != "All Branches (SMS + Email + URL)" else bench_samples // 3
                df_email = generate_benchmark_emails(n_branch)
                for _, r in df_email.iterrows():
                    tasks.append(("email", r["text"], r["label"]))

            if bench_channel in ["All Branches (SMS + Email + URL)", "URL Domain Inspector"]:
                n_branch = bench_samples if bench_channel != "All Branches (SMS + Email + URL)" else bench_samples // 3
                df_url = generate_benchmark_urls(n_branch)
                for _, r in df_url.iterrows():
                    tasks.append(("url", r["url"], r["label"]))

            for branch_type, text_input, label in tasks:
                total_samples += 1
                if branch_type == "sms":
                    res = predictor.predict_sms(text_input)
                elif branch_type == "email":
                    res = predictor.predict_email(text_input)
                else:
                    res = predictor.predict_url(text_input)

                pred_scam = (res["verdict"] == "SCAM")
                true_scam = (label == 1)

                if pred_scam and true_scam:
                    tp += 1
                    correct += 1
                elif not pred_scam and not true_scam:
                    tn += 1
                    correct += 1
                elif pred_scam and not true_scam:
                    fp += 1
                elif not pred_scam and true_scam:
                    fn += 1

            t_elapsed = time.time() - t_start
            accuracy = (correct / total_samples) * 100 if total_samples else 100.0
            precision = (tp / (tp + fp)) * 100 if (tp + fp) else 100.0
            recall = (tp / (tp + fn)) * 100 if (tp + fn) else 100.0
            f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 100.0
            avg_latency = (t_elapsed / total_samples * 1000) if total_samples else 0.0

            # Render metric cards
            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1:
                st.metric("Live Accuracy", f"{accuracy:.1f}%", delta=f"{correct}/{total_samples} correct")
            with mc2:
                st.metric("Live Recall (Cost-Sensitive)", f"{recall:.1f}%", delta=f"{fn} False Negatives")
            with mc3:
                st.metric("Live Precision", f"{precision:.1f}%", delta=f"{fp} False Positives")
            with mc4:
                st.metric("Mean Latency", f"{avg_latency:.1f} ms", delta=f"{total_samples / t_elapsed:.0f} req/sec")

            st.success(f"Benchmark completed in {t_elapsed:.2f}s across {total_samples} samples. Zero-day evasion defense active.")

    # 3. Adversarial & Zero-Day Evasion Challenge Suite
    st.markdown('<div class="card-title" style="font-size:1.25rem; margin-top:2rem;">Zero-Day & Adversarial Evasion Challenge</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-description">Test resistance against sophisticated evasive payloads: typosquats, brand impersonation, urgent BEC, and benign urgency.</div>', unsafe_allow_html=True)

    challenges = [
        {"Name": "Brand Typosquatting (.xyz TLD)", "Type": "URL", "Payload": "http://paypa1-security-update.xyz/auth/login", "Expected": "SCAM"},
        {"Name": "IP-Host Bypass with Port", "Type": "URL", "Payload": "http://192.168.1.105:8080/secure/bank.php", "Expected": "SCAM"},
        {"Name": "Executive Wire Fraud BEC", "Type": "Email", "Payload": "Subject: Wire Transfer Request - Strict Confidentiality\nPlease wire $48,500 immediately to the attached offshore escrow.", "Expected": "SCAM"},
        {"Name": "Benign Urgency False-Positive Check", "Type": "Email", "Payload": "Subject: Urgent: Quarterly Review Meeting in 15 mins\nTeam, please join the conference room immediately for our sprint retrospective.", "Expected": "BENIGN"},
        {"Name": "Smishing + Fake Link Fusion", "Type": "Compound", "Payload": "URGENT from Chase: Card compromised. Confirm identity now at http://secure-chase-update.xyz", "Expected": "SCAM"}
    ]

    run_adv_btn = st.button("Run Adversarial Evasion Suite", key="run_adv_btn")
    if run_adv_btn and predictor:
        adv_results = []
        for c in challenges:
            if c["Type"] == "URL":
                r = predictor.predict_url(c["Payload"])
                verdict = r["verdict"]
                conf = r["risk_score_pct"]
            elif c["Type"] == "Email":
                r = predictor.predict_email(c["Payload"])
                verdict = r["verdict"]
                conf = r["risk_score_pct"]
            else: # Compound
                r = predictor.predict_incident(email_text=c["Payload"], url="http://secure-chase-update.xyz")
                verdict = r["overall_verdict"]
                conf = r["overall_risk_score_pct"]

            passed = (verdict == c["Expected"])
            adv_results.append({
                "Challenge Vector": c["Name"],
                "Vector Type": c["Type"],
                "Expected": c["Expected"],
                "Model Verdict": verdict,
                "Threat Score": f"{conf}%",
                "Defense Status": "PASSED" if passed else "FAILED"
            })

        adv_th = "padding:9px 12px; text-align:left; border-bottom:1px solid rgba(255,255,255,0.15); color:#facc15; font-family:'Fira Code', monospace; font-size:0.82rem; text-transform:uppercase;"
        adv_td = "padding:9px 12px; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.85rem;"
        adv_html = f"""
        <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.1); border-radius:12px; overflow:hidden; margin-bottom:1.5rem;">
            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr style="background:rgba(255,255,255,0.03);">
                        <th style="{adv_th}">Challenge Vector</th>
                        <th style="{adv_th}">Type</th>
                        <th style="{adv_th}">Expected</th>
                        <th style="{adv_th}">Verdict</th>
                        <th style="{adv_th}">Score</th>
                        <th style="{adv_th}">Defense Status</th>
                    </tr>
                </thead>
                <tbody>
        """
        for row in adv_results:
            status_color = "#4ade80" if row["Defense Status"] == "PASSED" else "#f87171"
            adv_html += f"""
                    <tr>
                        <td style="{adv_td} font-weight:600; color:#e2e8f0;">{row['Challenge Vector']}</td>
                        <td style="{adv_td} color:#38bdf8;">{row['Vector Type']}</td>
                        <td style="{adv_td}">{row['Expected']}</td>
                        <td style="{adv_td} font-weight:600; color:{'#f87171' if row['Model Verdict']=='SCAM' else '#4ade80'};">{row['Model Verdict']}</td>
                        <td style="{adv_td}">{row['Threat Score']}</td>
                        <td style="{adv_td} font-weight:700; color:{status_color};">{row['Defense Status']}</td>
                    </tr>
            """
        adv_html += """
                </tbody>
            </table>
        </div>
        """
        st.markdown(adv_html, unsafe_allow_html=True)

    # 4. Architecture Foundation Cards
    col_m1, col_m2 = st.columns(2, gap="medium")
    with col_m1:
        st.markdown("""
        <div style="background:rgba(15, 23, 42, 0.6); border:1px solid rgba(255, 255, 255, 0.1); border-radius:16px; padding:1.25rem;">
            <h4 style="font-family:'Newsreader',serif; font-size:1.15rem; margin-top:0; color:#facc15;">Zero-Leakage Domain Splitting</h4>
            <p style="font-size:0.88rem; color:#94a3b8; line-height:1.5; margin-bottom:0;">
                Standard random train/test splits leak registered base domains across sets, causing models to memorize tokens rather than generalized structures. We enforce strict <code>GroupShuffleSplit</code> by base domain.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
        <div style="background:rgba(15, 23, 42, 0.6); border:1px solid rgba(255, 255, 255, 0.1); border-radius:16px; padding:1.25rem;">
            <h4 style="font-family:'Newsreader',serif; font-size:1.15rem; margin-top:0; color:#facc15;">Cost-Sensitive Thresholds</h4>
            <p style="font-size:0.88rem; color:#94a3b8; line-height:1.5; margin-bottom:0;">
                In cybersecurity, False Negatives carry devastating risk ($10K+ wire fraud / ransomware) compared to minor False Positive friction. Models are calibrated to prioritize Recall (&ge; 98%).
            </p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. Minimalist Footer
# -------------------------------------------------------------
st.markdown("""
<div style="text-align: center; padding: 3rem 0 1rem 0; color: #64748b; font-size: 0.85rem; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 3rem;">
    Whitehat AI Threat Intelligence System • Dynamic Net Grid Matrix Defense
</div>
""", unsafe_allow_html=True)
