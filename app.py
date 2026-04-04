import streamlit as st
from PIL import Image
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Microstructure of 0DTE | Quant Research",
    page_icon="line_chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a stark, academic, highly readable institutional whitepaper
st.markdown("""
    <style>
    /* Main container width and font stack */
    .main { max-width: 1100px; margin: 0 auto; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Typography Upgrades for Maximum Readability (Perfectly Balanced) */
    h1 { text-align: center; font-size: 2.8rem !important; font-weight: 900 !important; margin-bottom: 0.5rem !important; line-height: 1.25 !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.02em !important; }
    .subtitle { text-align: center; font-size: 1.3rem !important; color: var(--text-color) !important; opacity: 0.75 !important; font-style: italic !important; margin-bottom: 1.8rem !important; font-weight: 400 !important; }
    
    /* Elegant section spacing */
    h2 { font-weight: 800 !important; font-size: 2.2rem !important; margin-top: 2.8rem !important; border-bottom: 1px solid rgba(128, 128, 128, 0.2) !important; padding-bottom: 0.5rem !important; margin-bottom: 1.5rem !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.01em !important; }
    h3 { font-weight: 700 !important; font-size: 1.6rem !important; margin-top: 2rem !important; margin-bottom: 1rem !important; color: var(--text-color) !important; opacity: 0.95 !important; }
    
    /* Perfectly scaled body text (1.25rem is the sweet spot for long-form reading) */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li { 
        font-size: 1.25rem !important; 
        line-height: 1.6 !important; 
        font-weight: 400 !important; 
        color: var(--text-color) !important; 
        opacity: 0.9 !important; 
    } 
    div[data-testid="stMarkdownContainer"] strong { font-weight: 700 !important; color: var(--text-color) !important; opacity: 1 !important; }
    
    /* Elegant blockquotes instead of tinted background boxes */
    .callout { 
        border-left: 5px solid #3B82F6 !important; 
        padding-left: 1.25rem !important; 
        margin: 1.4rem 0 !important; 
        color: var(--text-color) !important; 
        font-size: 1.25rem !important; 
        background-color: transparent !important;
    }
    
    .quant-note { 
        border-left: 5px solid #10B981 !important; 
        padding-left: 1.25rem !important; 
        margin: 2rem 0 !important; 
        font-family: 'Courier New', Courier, monospace !important; 
        color: var(--text-color) !important; 
        font-size: 1.15rem !important;
        background-color: transparent !important;
    }
    
    .limitation-note {
        border-left: 5px solid #F59E0B !important; 
        padding-left: 1.25rem !important; 
        margin: 2rem 0 !important; 
        color: var(--text-color) !important; 
        font-size: 1.25rem !important;
        background-color: transparent !important;
    }
    
    /* Premium Regime Cards for Section 5 */
    .regime-card {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-radius: 8px !important;
        padding: 18px 22px !important;
        margin: 15px 0 !important;
        height: 100% !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }
    .regime-pin { border-top: 5px solid #3B82F6 !important; }
    .regime-break { border-top: 5px solid #EF4444 !important; }
    
    /* Custom Stat Boxes for KPI framing */
    .stat-box {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 8px !important;
        padding: 20px 15px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    
    .insight-box {
    border-left: 5px solid #8B5CF6 !important;
    padding-left: 1.25rem !important;
    margin: 1.4rem 0 !important;
    font-size: 1.25rem !important;
    }
    
    .stat-value { font-size: 2.4rem !important; font-weight: 800 !important; color: #3B82F6 !important; margin-bottom: 6px !important; line-height: 1 !important;}
    .stat-label { font-size: 0.95rem !important; font-weight: 600 !important; color: var(--text-color) !important; opacity: 0.7 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    
    /* Table of Contents Links *//* Main Section Badges */
    .section-badge {
        background-color: #2563EB;
        color: #FFFFFF !important;
        padding: 8px 16px;              
        border-radius: 8px;             
        font-size: 1.25rem;             
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        display: inline-block;
        vertical-align: middle;   
        margin-right: 12px;
    }
 
    .h2-text {
        position: relative;
        top: 3px;
    }
    
    
    .toc-link { text-decoration: none !important; font-size: 1rem !important; display: block !important; padding: 6px 0 !important; font-weight: 500 !important; color: var(--text-color) !important; opacity: 0.85 !important; transition: all 0.2s ease-in-out !important; }
    .toc-link:hover { color: #3B82F6 !important; opacity: 1 !important; }
    
    /* Image Styling */
    img { border-radius: 6px !important; border: 1px solid rgba(128, 128, 128, 0.15) !important; margin-bottom: 8px !important; }
    </style>
    
    
""", unsafe_allow_html=True)



# Helper function to load images safely
def load_image(image_name):
    try:
        return Image.open(image_name)
    except FileNotFoundError:
        return None

# ==========================================
# SIDEBAR: TABLE OF CONTENTS & AUTHOR
# ==========================================
st.sidebar.title("Table of Contents")
st.sidebar.markdown("""
<a href="#0-whats-really-happening-in-the-market" target="_self" class="toc-link">0. Intuition</a>
<a href="#1-executive-summary" target="_self" class="toc-link">1. Executive Summary</a>
<a href="#2-data-engineering-sanity-checks" target="_self" class="toc-link">2. Data Engineering & Sanity Checks</a>
<a href="#3-execution-friction-exposure-model" target="_self" class="toc-link">3. Execution Friction & Exposure Model</a>
<a href="#4-synthetic-volatility-surfaces" target="_self" class="toc-link">4. Synthetic Volatility Surfaces</a>
<a href="#5-regime-definitions-the-short-gamma-paradox" target="_self" class="toc-link">5. Regime Definitions & The Gamma Paradox</a>
<a href="#6-statistical-proof-signal-agreement" target="_self" class="toc-link">6. Statistical Proof & Signal Agreement</a>
<a href="#7-time-of-day-dynamics-theta-burnout" target="_self" class="toc-link">7. Time-of-Day Dynamics (Theta)</a>
<a href="#8-model-limitations" target="_self" class="toc-link">8. Model Limitations</a>
<a href="#9-conclusion-tech-stack" target="_self" class="toc-link">9. Conclusion</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Author:** Jayesh Chaudhary\n\n"
    "**Role:** Quantitative Researcher\n\n"
)

# ==========================================
# MAIN DOCUMENT: TITLE (HERO SECTION)
# ==========================================
st.markdown("<h1>Intraday Microstructure of 0DTE options: Market Maker Gamma Pins and Volatility Expansion</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>An Empirical Analysis of Dealer Positioning and Intraday Volatility.</p>", unsafe_allow_html=True)
# Small, muted author line under the subtitle
st.markdown("""
    <div style='text-align: center; margin-top: -1.0rem; margin-bottom: 3rem;'>
        <span style='font-size: 1.0rem; color: var(--text-color); opacity: 0.5; font-weight: 400; letter-spacing: 0.15em; text-transform: uppercase;'>
            Research by <strong>Jayesh Chaudhary</strong>
        </span>
    </div>
""", unsafe_allow_html=True)

# Quick Stats Bar
col_a, col_b, col_c, col_d = st.columns(4)

# Reusable green style templates for a pleasant, eye-friendly look
box_css = "background-color: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 20px 15px; text-align: center; margin-bottom: 20px;"
val_css = "font-size: 1.7rem; font-weight: 800; color: #10B981; margin-bottom: 6px; line-height: 1;"
lbl_css = "font-size: 0.90rem; font-weight: 600; color: var(--text-color); opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;"

with col_a:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Trading Days</div><div style='{val_css}'>107</div></div>", unsafe_allow_html=True)
with col_b:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Observations</div><div style='{val_css}'>37.2k</div></div>", unsafe_allow_html=True)
with col_c:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Data Sources</div><div style='{val_css}'>ES + SPX</div></div>", unsafe_allow_html=True)
with col_d:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Resolution</div><div style='{val_css}'>1m & EOD</div></div>", unsafe_allow_html=True)
    
# ==========================================
# SECTION 0: TLDR / INTUITION (CRITICAL)
# ==========================================
st.markdown("<h2 id='0-whats-really-happening-in-the-market'><span class='section-badge'>0. Intuition</span><span class='h2-text'> What’s Really Happening?</span></h2>", unsafe_allow_html=True)

st.markdown("""
Intraday price action often looks random, but when viewed through dealer positioning, clear structure emerges. Markets typically behave in two simple ways:

- **They remain near a high open-interest strike (price clustering behavior)**    
- **They break away and trend, with regime-dependent volatility behavior**

### Why this happens

It comes down to how **options dealers hedge risk**:

- When a large amount of options sit at a strike →  
  price tends to stay near that level as hedging activity stabilizes it

- When price moves far enough →  
  hedging flips → market **breaks and trends**
""")

st.markdown("""
<div class="callout">
<strong>What the Data Shows:</strong><br>

- **Pinned markets** → localized oscillation with lower realized variance  
- **Breakouts** → regime-dependent behavior, with both variance expansion and compression depending on time-of-day and liquidity

- **Gamma exposure** does not always increase volatility — its effect depends on the regime.  
  → it can suppress movement before a break, depending on regime

- **Theta** → dominates near the close  
  → forced unwinding creates volatility spikes

 In short: the market is usually being stabilized until it suddenly isn’t.
</div>
""", unsafe_allow_html=True)


st.markdown("""
**Key Takeaways:**

• Dealer positioning creates measurable intraday structure in price behavior<br>
• Pinning regimes are associated with variance compression (<1)<br>
• Breakout regimes are non-uniform and strongly time-of-day dependent<br>
• • Relying on yesterday's closing data is insufficient; calculating exposure minute-by-minute is required to see the true intraday structure.
""", unsafe_allow_html=True)

# ==========================================
# SECTION 1: EXECUTIVE SUMMARY
# ==========================================
st.markdown("<h2 id='1-executive-summary'><span class='section-badge'>1. Summary</span><span class='h2-text'> What This Project Does</span></h2>", unsafe_allow_html=True)

st.markdown("""
0DTE options now dominate intraday index trading, which makes dealer hedging flows a measurable component of intraday price dynamics.
Market makers are constantly adjusting their positions, and this hedging flow directly interacts with the underlying futures market.
This project measures how dealer hedging affects intraday volatility.

""")

st.markdown("""
The study analyzes 107 trading days using 1-minute price snapshots (yielding ~37,000 discrete intraday observations). This high-frequency dataset allows us to observe both immediate minute-to-minute hedging impacts, as well as broader time-of-day trends.
""")


# ==========================================
# SECTION 2: DATA ENGINEERING
# ==========================================





st.markdown("<h2 id='2-data-engineering-sanity-checks'><span class='section-badge'>2. Data</span><span class='h2-text'> Engineering & Sanity Checks</span></h2>", unsafe_allow_html=True)

st.markdown("""
The pipeline reconstructs intraday dealer positioning from EOD options data and futures prices.
""")

with st.expander("Pipeline Overview (Click to Expand)"):
    st.markdown("""
    The workflow follows a strict intraday reconstruction pipeline:

    **1. EOD Initialization**  
    Start with the static End-of-Day (EOD) SPX options chain from the day *prior* to expiration.
    
    **2. Intraday Alignment**  
    Because tick-level options data is prohibitively massive, we map the static EOD options against the live 1-minute S&P 500 (ES) futures price path for the current trading day.

    **3. Dynamic Repricing**  
    For every 1-minute interval, we use Black-Scholes and "Sticky Moneyness" to recalculate what the options *should* be priced at based on the new futures price. We are effectively creating a simulated intraday option chain.

    **4. Gamma Construction**  
    Sum up the recalculated dealer gamma exposure across all strikes for every minute.

    **5. Regime Identification**  
    Categorize the market state by measuring how close the price is to high Open Interest (OI) strikes, and calculating the curvature of the Implied Volatility (IV) surface to pinpoint exactly where dealers are concentrated.

    **6. Statistical Evaluation**  
    Evaluate forward return distributions (1m–30m horizons)

    ---
    This ensures all signals are forward-looking and free from look-ahead bias.
    """)

st.markdown("""
Microstructure models are highly sensitive to data quality, so the pipeline enforces strict filtering and validation before any modeling.

""")

with st.expander("View Data Cleaning & Validation Details"):
    st.markdown("""
    **Transformations & Validations Applied:**
    * **Strict Lookback Logic:** To prevent look-ahead bias, the options universe is constructed exclusively using data from the market close on the day *before* the 0DTE expiration. Any contracts that have already expired (DTE < 1) are filtered out.
    * **Arbitrage Bounds:** Eliminated 14,027 records that violated standard pricing physics (e.g., Deltas > 1.0, negative Gamma, or Implied Volatility > 500%).
    * **Skew Confirmation:** Verified that Out-of-the-Money (OTM) Puts traded at a higher implied volatility than At-the-Money (ATM) options. This confirms a structurally sound "Volatility Skew" before proceeding.
    """)

st.markdown("""
<div class="quant-note">
<strong>Exogenous Event Filter:</strong><br>
The pipeline explicitly removed 18 macro events spanning 15 trading days (e.g., FOMC rate decisions, CPI prints). Fundamental macro news naturally overrides normal order book dynamics. Blacking out these dates ensures the variance observed is mechanically driven by the options market, rather than fundamental repricing.
</div>
""", unsafe_allow_html=True)


# ==========================================
# SECTION 3: EXECUTION FRICTION
# ==========================================
st.markdown("<h2 id='3-execution-friction-exposure-model'><span class='section-badge'>3. Model</span><span class='h2-text'> Execution Friction & Exposure</span></h2>", unsafe_allow_html=True)

st.markdown("""
Dealer hedging is discrete, not continuous. Execution is constrained by transaction costs and liquidity, so small price moves are often ignored.
""")

st.markdown("""
Empirically, dealers do not hedge every single tick. In our simulation, they only execute hedges when the price moves past the bid-ask spread (which we call the "friction band"). Because of this assumed buffer, hedging was triggered in only ~50% of the 1-minute intervals; minor price noise was simply absorbed without forcing a trade.
""")

with st.expander("View Exposure Normalization & Friction Model Details"):
    st.markdown("""
    ### Dealer Inventory Assumption ("All Short")
    Because public feeds do not identify who bought or sold an option, this model applies the standard 0DTE "All Short" assumption. We assume retail traders are the aggressive buyers of both Calls and Puts, forcing Market Makers (Dealers) to take the other side, resulting in a net Short Gamma profile for the street.        
        
    ### Exposure Normalization
    
    During model initialization (August 17, 2022), the gamma aggregation revealed a heavy skew toward downside protection:
    * **Call Gamma Exposure:** -$177.19 Million
    * **Put Gamma Exposure:** -$3.80 Billion
    * **Net Dealer Gamma:** -$3.98 Billion
    
    **What does this mean?**: These represent **Gamma Notional**—an estimate of the total dollar amount dealers must buy or sell in the futures market if the index moves by 1%. It is calculated by aggregating the theoretical gamma of every open contract multiplied by the spot price and open interest.
    From above numbers, dealers were theoretically forced to sell nearly $4 Billion in futures to stay hedged. 
    To understand the true market impact, I normalized this $4 Billion against the actual average daily volume of the ES futures market. The resulting percentage was massive, confirming that on heavy expiry days, dealer hedging requirements are large enough to overwhelm normal liquidity and significantly impact price direction.


    ### Friction Mechanics
    Dealers execute hedges solely when their directional risk exceeds the cost of crossing the spread. Example:
    * `Starting Anchor Price: 4000.00`
    * `Friction Band: +/- 1.00 points` (Dealers ignore minor fluctuations inside this band).
    * `Market moves to 4000.50 -> Hedge Triggered?` **False**
    * `Market moves to 4001.10 -> Hedge Triggered?` **True** (New Anchor Price is set, and hedging flow reaches the order book).
    """)
    
st.markdown("""
<div class="quant-note">
<strong>Scale of Exposure:</strong><br>
On representative days, aggregate dealer gamma is on the order of billions of dollars notional, often exceeding underlying futures volume when normalized.<br><br>
→ This creates conditions where relatively small price changes can require disproportionately large hedge adjustments.
</div>
""", unsafe_allow_html=True)

# # Custom Dashboard Metrics
# col5, col6, col7 = st.columns(3)
# with col5:
#     st.markdown("<div class='stat-box'><div class='stat-value'>361</div><div class='stat-label'>Total Trading Minutes</div></div>", unsafe_allow_html=True)
# with col6:
#     st.markdown("<div class='stat-box'><div class='stat-value'>190</div><div class='stat-label'>Forced Hedge Triggers</div></div>", unsafe_allow_html=True)
# with col7:
#     st.markdown("<div class='stat-box'><div class='stat-value'>171</div><div class='stat-label'>Dealer Holding (Ignored)</div></div>", unsafe_allow_html=True)




# ==========================================
# SECTION 4: SYNTHETIC VOLATILITY SURFACES
# ==========================================
st.markdown("<h2 id='4-synthetic-volatility-surfaces'><span class='section-badge'>4. Engine</span><span class='h2-text'> Dynamic Intraday Repricing</span></h2>", unsafe_allow_html=True)

st.markdown("""
<div class="callout">
<strong>The Engineering Constraint:</strong> Tick-level historical options data is prohibitively expensive and massive. Therefore, relying on static End-of-Day (EOD) data is standard, but that data goes stale the minute the market opens.
<strong>The Solution:</strong> This pipeline builds a dynamic repricing engine. As the 1-minute futures price moves, the model mathematically adjusts the options surface to track real-time dealer exposure without requiring tick-level options feeds.
</div>
""", unsafe_allow_html=True)

st.markdown("""
EOD gamma becomes unreliable intraday because implied volatility changes continuously, so the model reprices the surface each minute to maintain consistent exposure estimates.

### 1. Sticky Moneyness
I constructed a dynamic Volatility Surface that shifts concurrently with the underlying spot price. The engine recalculates Black-Scholes Gamma for every option each minute using vectorized repricing.
""")

st.markdown("""
### 2. Identifying "Pins" via Curvature
To mathematically locate where dealers are most concentrated, I calculated the local curvature of the IV surface using a discrete second derivative approximation:
""")
st.latex(r"Curvature \approx IV_{K-\Delta K} + IV_{K+\Delta K} - 2 \cdot IV_{K}")
st.markdown("""
A highly convex curve indicates heavy dealer concentration at a specific strike price. This creates a gravitational pull on the underlying asset, often referred to mechanically as a **"Pin."**
""")
    
st.markdown("""
This plot serves as a sanity check confirming the expected monotonic Volatility Skew under sticky moneyness. While the macro-level curve appears linear from a distance, calculating the discrete second derivative reveals *micro-level convexity* (localized bumps). These highly convex bumps indicate heavy dealer concentration at specific strikes, creating a gravitational pull on the underlying asset known as a **"Pin."**
""")


# ==========================================
# SECTION 5: REGIME DEFINITION
# ==========================================
st.markdown("<h2 id='5-regime-definitions-the-short-gamma-paradox'><span class='section-badge'>5. Regimes</span><span class='h2-text'> Definitions & The Gamma Paradox</span></h2>", unsafe_allow_html=True)

st.markdown("""
**The Gamma Paradox:** Retail traders often assume heavy "Short Gamma" positioning immediately guarantees explosive market volatility. However, the data reveals a paradox: heavy dealer concentration often acts as a massive localized magnet, **compressing** volatility (Pinning) until the market escapes the gravity well (Breaking).
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="regime-card regime-pin">
        <h3 style="margin-top: 0;">🧲 Synthetic Pinning (price clusters near a high open-interest strike)</h3>
        
    <p><strong>Definition:</strong> Underlying futures price remains trapped near a high-interest options strike.</p></p>
    <p><strong>Behavior:</strong> Short-term oscillation, but overall movement constrained</p>
    <p><strong>Data:</strong> Variance compression (lower than normal volatility) across most horizons</p>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="regime-card regime-break">
        <h3 style="margin-top: 0;">💥 Synthetic Breaking (price escapes and trends)</h3>
        
    <p><strong>Definition:</strong> Underlying futures price escapes the gravitational pull of a concentrated strike region.</p>
    <p><strong>Behavior:</strong> Directional moves with regime-dependent volatility</p>
    <p><strong>Data:</strong> Strong expansion at the open (peaking near ~3x in intraday buckets), neutral/compressive later</p>
    </div>
    """, unsafe_allow_html=True)
    

    
st.markdown("""
<div class="insight-box">
<strong>Strike Gravity Observation:</strong><br>
The majority of observations occur near high open-interest strikes, indicating that price spends most of its time in "pinned" regions rather than freely trending.
</div>
""", unsafe_allow_html=True)
    




# ==========================================
# SECTION 6: STATISTICAL PROOF
# ==========================================
st.markdown("<h2 id='6-statistical-proof-signal-agreement'><span class='section-badge'>6. Stats</span><span class='h2-text'> Proof & Signal Agreement</span></h2>", unsafe_allow_html=True)

with st.expander("Methodology Note: Ensuring Statistical Rigor"):
    st.markdown("""
    * **Discarding Mean Return Tests:** Forward mean returns in High-Frequency Trading (HFT) data approach zero. This model tests the shape and variance of the distribution exclusively.
    * **Strict Forward Returns:** All statistical tests exclusively measure *forward-looking* log returns (e.g., price change from $T$ to $T+15$). We never use backward-looking shifts, which prevents data leakage and look-ahead bias.
    * **Multi-Horizon Testing:** 1m, 5m, 15m, and 30m forward returns were analyzed concurrently to eliminate localized curve-fitting.
    """)

st.markdown("""
**Active Gamma:** minutes where dealer hedging is triggered  
**Baseline:** normal minutes with no forced hedging
""")

st.markdown("### Core Result: Active Gamma vs Baseline (Forward Returns: 1m–30m)")
st.markdown("""
**Each row shows forward returns over that horizon** (e.g., 5m = next 5-minute return)
""")

st.markdown("""
| Horizon | N Active | N Baseline | Var Ratio | KS p | Levene p | Kurtosis Δ | Mean (bps) | T-test p |
|--------|----------|------------|----------|------|----------|------------|------------|----------|
| 1m | 3540 | 33551 | 0.66 | 0.005 | 0.004 | -834 | -0.05 | 0.706 |
| 5m | 3538 | 33545 | 0.87 | 0.212 | 0.008 | -169 | 0.35 | 0.253 |
| 15m | 3530 | 33533 | 0.76 | 0.087 | 0.402 | -55 | 0.87 | 0.084 |
| 30m | 3517 | 33516 | 0.79 | 0.054 | 0.670 | -25 | 2.57 | 0.0004 |
""")

st.markdown("""
<div class="callout">

<strong>How to Read This:</strong><br>

Values compare volatility during Active Gamma periods vs normal periods.

• 0.66 → 34% lower than normal  
• 1.30 → 30% higher than normal  
</div>
""", unsafe_allow_html=True)


st.markdown("""
At the 1-minute level, volatility during active hedging is ~34% lower than normal (0.66x), indicating short-term stabilization.
""")

img_dist = load_image("images/kde_grid.png")
if img_dist: 
    st.image(img_dist, caption="KDE Distributions across horizons. Notice the structural differences in tail risk between regimes.", use_container_width=True)



st.markdown("### Strike Gravity Distribution")

st.markdown("""
| Location | Count |
|----------|------|
| Near Heavy Strike | 36,250 |
| Far From Heavy Strike | 843 |
| Unknown | 90 |

*(Note: "Heavy Strike" is defined as the top 20% of strikes by Open Interest. "Near" is defined as price being within ±0.5% of that strike).*
""")

st.markdown("""
Most observations occur near high open-interest strikes, confirming that the dataset is heavily dominated by pinned regimes rather than free-trending behavior.
""")

    
st.markdown("### EOD vs. Synthetic Gamma Agreement")
st.markdown("""
To validate the repricing engine, I compared the classic "Static EOD" regime labels against my dynamic "Synthetic" regime labels minute-by-minute.
Static EOD gamma can lag the market. The results show that static EOD gamma lags the market. In about 20% of observations, the two signals disagree. When both signals *agree* (e.g., both indicate a breakout), the statistical significance of the volatility move is much stronger.
""")

col3, col4 = st.columns(2)
with col3:
    img_line = load_image("images/eod_vs_syn_line.png")
    if img_line: st.image(img_line, use_container_width=True)
with col4:
    img_bar = load_image("images/syn_bar_chart.png")
    if img_bar: st.image(img_bar, use_container_width=True)
    
    
st.markdown("""
### Pinning vs Breaking (30-Minute Synthetic Horizon)

<div class="callout">
<strong>Results (based on 30-minute forward returns):</strong><br>

<strong>Synthetic Pinning:</strong><br>
• Variance ≈ 1.52x (≈52% higher than normal)<br>
• KS p = 0.0000 (Statistically significant distribution shift)<br><br>

<strong>Synthetic Breaking:</strong><br>
• Variance ≈ 0.84x (≈16% lower than normal)<br>
• KS p = 0.0000 (Statistically significant distribution shift)<br><br>


</div>
""", unsafe_allow_html=True)   

st.markdown("""
👉 Interpretation:<br>
When using high-resolution synthetic intraday data, the traditional "pinning equals low volatility" assumption flips at longer time horizons. True intraday pinning actually exhibits <em>higher</em> variance than normal noise, likely due to violent mean-reverting chop around the strike. Conversely, true breakouts exhibit a smoother, lower-variance directional glide.
""", unsafe_allow_html=True)

st.markdown("""
The common assumption is that short gamma leads to higher volatility, but the data does not support this uniformly.
""")

st.markdown("""
<div class="insight-box">
<strong>Key Microstructure Observations:</strong><br>
• <strong>Short-Horizon Compression:</strong> At the 1-minute level, active hedging compresses volatility to ~0.66x of normal.<br>
• <strong>Time-Decay of Signal:</strong> This compression is strongest at microstructure horizons (1–5 minutes) and weakens as time aggregates, confirming dealer effects are short-lived.<br>
• <strong>Passive Dominance:</strong> Gamma-driven hedging triggers in only ~10% of observations. The vast majority of intraday price action occurs in passive regimes where dealers are holding, not hedging.<br>
• <strong>Greek Hierarchy:</strong> Delta (linear exposure) shows limited impact on variance, proving that Gamma (convexity) and Theta (decay) are the true drivers of intraday structural shifts.
</div>

""", unsafe_allow_html=True)


with st.expander("Delta Dominance Results (Linear Exposure)"):
    st.markdown("""
This tests whether **delta (linear hedging)** changes volatility.

Result: delta has minimal impact compared to gamma.

| Horizon | Var Ratio | KS p | Levene p | Mean (bps) |
|--------|----------|------|----------|------------|
| 1m | 0.92 | 0.000 | 0.0012 | 0.09 |
| 5m | 0.92 | 0.000 | 0.0049 | 0.49 |
| 15m | 0.92 | 0.000 | 0.0032 | 1.36 |
| 30m | 1.06 | 0.000 | 0.3159 | 3.14 |

→ Interpretation: delta slightly shifts distribution but does not materially change volatility.
""")

with st.expander("Theta Dominance (Expiry Effect)"):
    st.markdown("""
This isolates **time decay effects near expiry**.

| Horizon | Var Ratio | KS p | Levene p |
|--------|----------|------|----------|
| 1m | ~1.4–1.6 | ~0.000 | ~0.001 |
| 30m | ~1.7 | ~0.000 | ~0.001 |

→ Interpretation: Because Theta (time decay) accelerates exponentially in the final hours of a 0DTE session, "Theta Dominance" isolates late-day trading. The data proves volatility increases significantly near the close (1.7x) due to forced position unwinding.
""")





st.markdown("""
<div class="callout">
<strong>Model Validation Perspective:</strong><br>

👉 Interpretation:  
Because static EOD signals diverge from dynamic synthetic signals in 20% of intraday observations, relying solely on stale End-of-Day data mathematically misrepresents real-time dealer exposure. Intraday repricing is a strict requirement for accurate modeling.
</div>
""", unsafe_allow_html=True)




with st.expander("Detailed Statistical Results (KS & Levene Tests)"):
    st.markdown("""
    **Statistical Significance Highlights (15-Minute Synthetic Data):**
    * **Synthetic Pinning:** Variance Ratios vary by context but are predominantly <1, indicating compression in most regimes. KS p-value = `0.0000`, verifying that the distribution shape statistically broadens.
    * **Synthetic Breaking:** Variance ratios are regime-dependent (≈0.8–3.0 across contexts). KS p-value = `0.0001`, verifying statistically significant distribution shifts.
    """)




# ==========================================
# SECTION 7: TIME-OF-DAY DYNAMICS
# ==========================================
st.markdown("<h2 id='7-time-of-day-dynamics-theta-burnout'><span class='section-badge'>7. Temporal</span><span class='h2-text'> Time-of-Day Dynamics</span></h2>", unsafe_allow_html=True)

st.markdown("""
Because 0DTE options decay to zero by 4:00 PM, dealers have less room to carry risk into the close. That makes late-session hedging more forced and more volatile.
""")


st.markdown("""
<div class="callout" style="border-left-color: #EF4444;">
<strong>The Impact of Theta (Time Decay):</strong><br>
Isolating regimes dominated by Theta revealed some of the highest realized variance in the dataset:
<ul style="margin-top: 5px; margin-bottom: 5px;">
    <li><strong>Volatility Multiplier:</strong> Expanded to 1.70x at the 30-minute horizon.</li>
    <li><strong>Kurtosis (Tail Risk):</strong> Increased by +585.38 at the 1-minute horizon (p-value = 0.0004).</li>
</ul>
As expiry approaches, dealers unwind positions, increasing volatility. The effect is strongest near close and depends on liquidity conditions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
These effects are not uniform — they vary significantly across time-of-day and global trading sessions.
""")


col5, col6 = st.columns(2)
with col5:
    img_h1 = load_image("images/heatmap_intra_squeeze.png")
    if img_h1: st.image(img_h1, caption="Intraday Trend/Breakout Variance", use_container_width=True)
    
    img_h2 = load_image("images/heatmap_global_squeeze.png")
    if img_h2: st.image(img_h2, caption="Global Session Trend Variance", use_container_width=True)
    
with col6:
    img_h3 = load_image("images/heatmap_intra_pin.png")
    if img_h3: st.image(img_h3, caption="Intraday Pin/Chop Variance", use_container_width=True)
    
    img_h4 = load_image("images/heatmap_global_pin.png")
    if img_h4: st.image(img_h4, caption="Global Session Pin Variance", use_container_width=True)


st.markdown("""
**Session read:** Asia handoff shows the clearest pinning compression, London/US overlap is mixed, and US-only is the least pinned and often expansionary in this sample. So the same regime behaves differently depending on the session — the label alone is not enough.
""")

st.markdown("""
*Observation: Breakout volatility multipliers are notably amplified right at the OPEN. Dealers must actively hedge structural gaps from the overnight session before intraday liquidity normalizes.*
""")

st.markdown("""
### Key Structural Observation

The strength of these effects is highly time-dependent:

- **Market Open:** strongest breakout expansion (consistent with hedging of overnight gaps)  
- **Midday:** weakest signal (liquidity stabilizes flows)  
- **Late Session:** pinning and theta-driven effects dominate  

👉 This shows that dealer-driven microstructure is not constant, it depends on liquidity regime and time-of-day.
""")

# ==========================================
# SECTION 8: MODEL LIMITATIONS
# ==========================================
st.markdown("<h2 id='8-model-limitations'><span class='section-badge'>8. Limits</span><span class='h2-text'> Model Limitations</span></h2>", unsafe_allow_html=True)

st.markdown("""
<div class="limitation-note">
<strong>What This Model Cannot Infer:</strong><br>
To maintain structural rigor, it is critical to explicitly define the boundaries of this research:
<ul style="margin-top: 5px; margin-bottom: 5px;">
    <li><strong>Non-Directionality:</strong> Gamma is a non-directional, second-order Greek. This model predicts the <em>compression or expansion of variance</em>, not the <em>directional vector</em> (up or down) of the breakout.</li>
    <li><strong>Macroeconomic Overrides:</strong> The model is purely microstructural. It fails during macroeconomic surprises where fundamental repricing overrides order book gravity (which necessitated the strict blackout filter).</li>
    <li><strong>Causality vs. Catalyst:</strong> While dealer positioning dictates the "pinning gravity" of the market, exogenous directional flow (e.g., institutional or retail buying) remains the ultimate catalyst required to break a pin.</li>
</ul>
</div>
""", unsafe_allow_html=True)


# ==========================================
# SECTION 9: CONCLUSION
# ==========================================
st.markdown("<h2 id='9-conclusion-tech-stack'><span class='section-badge'>9. Final</span><span class='h2-text'> Conclusion</span></h2>", unsafe_allow_html=True)

st.markdown("""
### The Bottom Line
Intraday volatility is not purely random — a measurable percentage of it reflects the mechanics of how risk is transferred and managed in the options market. Dealer positioning dictates the "gravity" of the market, while time-of-day dictates the "urgency."

**Key Results:**
* **Gamma acts as a dampener, not just an accelerator:** Short-horizon variance compresses (~0.66x at 1m) during active hedging. 
* **Regimes matter:** Pinning creates violent localized mean-reversion, while breakouts create directional glides.
* **Theta is the ultimate catalyst:** Late-session forced unwinding creates the most significant volatility expansion (~1.7x) of the day.
* **EOD is stale:** Minute-by-minute synthetic repricing is required to see these dynamics, as EOD positioning diverges from reality 20% of the time.
""")


st.markdown("### Core Competencies & Tech Stack")

st.markdown("""
* **Languages & Frameworks:** Python, Pandas, NumPy, SciPy, Seaborn, Streamlit.
* **Quantitative Concepts:** * Black-Scholes-Merton Pricing & Option Greeks (Gamma/Delta/Theta).
  * Volatility Surface Interpolation, Extrapolation & Curvature Math.
  * Discrete Derivatives & Market Microstructure (Friction/Bid-Ask Modeling).
* **Statistical Methods:** * Levene’s Test for Homogeneity of Variance.
  * Kolmogorov-Smirnov (KS-2Samp) Distribution Shape Testing.
  * Out-of-Sample Forward Log Returns.
* **Data Engineering:** * Efficient vectorized data processing and simulation.
  * Strict avoidance of time-series look-ahead and reversal bias corruption.
""")

st.markdown("""
👉 Intraday volatility is not purely random — a meaningful part of it reflects how dealers manage risk and rebalance exposure in real time.
In other words, intraday price behavior is not just noise — it reflects the mechanics of how risk is transferred and managed in the options market.
""")



st.markdown("""
<div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(128, 128, 128, 0.2);'>
    <p style='font-size: 1.15rem; color: #6B7280; font-style: italic;'>
        If you made it all the way to the end, thank you for viewing my work. <br>
        I am always looking to refine these projects, so if you have critiques, suggestions, or just want to talk market dynamics, I'd love to hear them:
    </p>
    <a href='mailto:jayeshchaudharyofficial@gmail.com' style='font-size: 1.15rem; font-weight: 700; color: #FFFFFF; background-color: #3B82F6; padding: 10px 24px; border-radius: 6px; text-decoration: none; display: inline-block; transition: all 0.2s;'>
        ✉️ Email Me
    </a>
</div>
""", unsafe_allow_html=True)