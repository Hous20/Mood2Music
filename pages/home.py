import streamlit as st

# CSS avec masquage du contenu HTML
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* Masquer les elements Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.stApp > div:first-child { padding-top: 0; }
.main .block-container { padding: 0; max-width: 100%; }

/* Forcer le conteneur principal à prendre tout l'espace */
.stApp {
    background: transparent !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: none !important;
    width: 100% !important;
    background: transparent !important;
}

/* Variables */
:root {
    --primary: #1DB954;
    --accent: #1ed760;
}

/* Page hero complète - RETOUR VERSION SIMPLE */
.hero-page {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-size: 400% 400%;
    animation: gradient-move 15s ease infinite;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    font-family: 'Poppins', sans-serif;
    overflow: hidden;
    padding: 1rem;
    width: 100%;
}

/* Bloc principal avec contour visuel - VERSION STABLE */
.main-content-block {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(25px);
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 40px;
    padding: 6rem 4rem;
    box-shadow: 0 30px 100px rgba(0, 0, 0, 0.4);
    text-align: center;
    width: 85%;
    max-width: 1000px;
    min-height: 70vh;
    position: relative;
    animation: block-appear 1s ease-out;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 2rem auto;
    z-index: 2;
}

@keyframes block-appear {
    from { opacity: 0; transform: translateY(30px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes gradient-move {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Titre principal - Plus large et mieux centré */
.main-title {
    font-size: 5.5rem;
    font-weight: 700;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: text-gradient 3s ease infinite;
    text-align: center;
    margin: 0 0 1rem 0;
    width: 100%;
    letter-spacing: 2px;
    text-shadow: 0 0 40px rgba(255,255,255,0.3);
}

@keyframes text-gradient {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Slogan - Plus visible et espacé */
.hero-slogan {
    font-size: 2.2rem;
    color: white;
    text-align: center;
    margin: 1rem 0;
    opacity: 0.95;
    font-weight: 300;
    text-shadow: 0 3px 6px rgba(0,0,0,0.4);
    letter-spacing: 1px;
}

/* Description - Plus large et mieux positionnée */
.hero-desc {
    font-size: 1.4rem;
    color: rgba(255,255,255,0.85);
    text-align: center;
    margin: 1.5rem auto 3rem auto;
    max-width: 800px;
    line-height: 1.6;
    padding: 0 2rem;
}

/* Egaliseur musical */
.music-eq {
    display: flex;
    justify-content: center;
    gap: 3px;
    margin: 2rem 0;
    height: 40px;
    align-items: flex-end;
}

.eq-bar {
    width: 4px;
    background: linear-gradient(to top, var(--primary), var(--accent));
    border-radius: 2px;
    animation: equalizer 1.5s ease-in-out infinite;
}

.eq-bar:nth-child(1) { animation-delay: 0s; }
.eq-bar:nth-child(2) { animation-delay: 0.1s; }
.eq-bar:nth-child(3) { animation-delay: 0.2s; }
.eq-bar:nth-child(4) { animation-delay: 0.3s; }
.eq-bar:nth-child(5) { animation-delay: 0.4s; }

@keyframes equalizer {
    0%, 100% { height: 10px; }
    50% { height: 35px; }
}

/* Icones flottantes */
.floating-icon {
    position: absolute;
    font-size: 2rem;
    opacity: 0.3;
    color: white;
    animation: float-around 6s ease-in-out infinite;
    pointer-events: none;
}

.floating-icon:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
.floating-icon:nth-child(2) { top: 30%; right: 15%; animation-delay: 2s; }
.floating-icon:nth-child(3) { bottom: 30%; left: 20%; animation-delay: 4s; }
.floating-icon:nth-child(4) { bottom: 20%; right: 10%; animation-delay: 1s; }

@keyframes float-around {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-20px) rotate(5deg); }
    66% { transform: translateY(10px) rotate(-5deg); }
}

/* Style du bouton Streamlit */
.stButton > button {
    background: linear-gradient(45deg, var(--primary), var(--accent)) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 18px 45px !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    font-family: 'Poppins', sans-serif !important;
    box-shadow: 0 8px 25px rgba(29, 185, 84, 0.4) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin-top: 2rem !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 35px rgba(29, 185, 84, 0.6) !important;
}

/* Conteneur du bouton - pour l'espacement avec le bloc */
.stButton {
    margin-top: 3rem !important;
    position: relative;
    z-index: 10;
}

/* Footer */
.hero-footer {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: rgba(255,255,255,0.7);
    font-size: 0.9rem;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    z-index: 10;
}

/* Gestion de la sidebar - Garder le plein écran */
/* Supprimé temporairement pour éviter les conflits */

/* Variables CSS pour la sidebar */
:root {
    --sidebar-width: 21rem;
}

/* Responsive - Version plein écran */
@media (max-width: 768px) {
    .hero-page { 
        padding: 0;
    }
    .main-content-block {
        width: 100%;
        padding: 4rem 2rem;
        min-height: 100vh;
        border-radius: 0;
    }
    .main-title { 
        font-size: 3.5rem; 
        letter-spacing: 1px;
    }
    .hero-slogan { 
        font-size: 1.6rem;
        margin: 0.8rem 0;
    }
    .hero-desc { 
        font-size: 1.1rem;
        max-width: 100%;
        padding: 0 1rem;
    }
}

@media (max-width: 480px) {
    .main-content-block {
        width: 100%;
        padding: 3rem 1.5rem;
        min-height: 100vh;
        border-radius: 0;
    }
    .main-title { 
        font-size: 2.8rem;
        letter-spacing: 0.5px;
    }
    .hero-slogan { font-size: 1.4rem; }
    .hero-desc { 
        font-size: 1rem;
        padding: 0 0.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Contenu principal (rendu dans le hero CSS)
st.html("""
<div class="hero-page">
    <div class="floating-icon">🎵</div>
    <div class="floating-icon">🎶</div>
    <div class="floating-icon">🎧</div>
    <div class="floating-icon">🎤</div>
    
    <div class="main-content-block">
        <h1 class="main-title">Mood2Music</h1>
        <p class="hero-slogan">Ressentez la musique</p>
        <p class="hero-desc">Découvrez la bande sonore parfaite pour chaque émotion</p>
        
        <div class="music-eq">
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
            <div class="eq-bar"></div>
        </div>
    </div>
</div>

<div class="hero-footer">
    ✨ Propulsé par Spotify API • Plus de 6000 genres musicaux ✨
</div>
""")

# Bouton centre (en dehors du hero pour etre fonctionnel)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎵 Decouvrir la musique", key="main_btn", use_container_width=True):
        st.switch_page("pages/landing_page.py")