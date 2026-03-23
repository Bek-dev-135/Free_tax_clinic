import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Free Tax Clinics Near Burnaby, BC",
    page_icon="🍁",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #1a3a4a 0%, #0d2233 60%, #1a3a4a 100%);
    color: #f5f0e8;
    padding: 2rem 2.5rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: "🍁";
    position: absolute;
    right: 2rem;
    top: 1rem;
    font-size: 5rem;
    opacity: 0.12;
}
.main-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    margin: 0 0 0.3rem;
    color: #f5f0e8;
    letter-spacing: -0.5px;
}
.main-header p {
    margin: 0;
    color: #a8c4d0;
    font-size: 0.95rem;
    font-weight: 300;
}

.filter-card {
    background: #f9f6f1;
    border: 1px solid #e0d8cc;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.filter-card h4 {
    font-family: 'DM Serif Display', serif;
    color: #1a3a4a;
    margin: 0 0 0.8rem;
    font-size: 1.05rem;
}

.legend-box {
    background: #fff;
    border: 1px solid #e0d8cc;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #444;
}
.legend-box h4 {
    font-family: 'DM Serif Display', serif;
    color: #1a3a4a;
    margin: 0 0 0.6rem;
}
.legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
.dot { width: 13px; height: 13px; border-radius: 50%; flex-shrink: 0; }

.clinic-count {
    background: #1a3a4a;
    color: #f5f0e8;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.88rem;
    text-align: center;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Clinic Data ───────────────────────────────────────────────────────────────
clinics = [
    {
        "name": "Glen Pine Pavilion (Burnaby Homeless Tax Clinics)",
        "address": "1200 Glen Pine Ct, Coquitlam, BC",
        "distance": "3.5 km",
        "type": "Walk-in",
        "languages": "English, Cantonese, German, Japanese",
        "clientele": "2SLGBTQI+ friendly, Housing insecure, Indigenous, Newcomers, Seniors",
        "returns": "Current and prior years",
        "lat": 49.2693, "lon": -122.8287,
        "phone": "604-299-5844",
        "website": "https://www.canadahelps.org/en/charities/burnaby-homeless-outreach-society/",
    },
    {
        "name": "KCWN 2026 Free Income Tax Clinic",
        "address": "4061 Kingsway, Burnaby, BC",
        "distance": "10.1 km",
        "type": "Walk-in",
        "languages": "English, Hindi, Korean",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2288, "lon": -122.9788,
        "phone": "604-436-1025",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "SHARE Tax Clinic",
        "address": "500-2755 Lougheed Hwy, Port Coquitlam, BC",
        "distance": "10.8 km",
        "type": "By appointment",
        "languages": "English, Cantonese, Hindi, Mandarin",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2620, "lon": -122.7810,
        "phone": "604-540-9161",
        "website": "https://sharesociety.ca/",
    },
    {
        "name": "Burnaby Homeless Tax Clinics (Kingsway)",
        "address": "7375 Kingsway, Burnaby, BC",
        "distance": "11.2 km",
        "type": "Drop-off",
        "languages": "English",
        "clientele": "Residents, Seniors",
        "returns": "Current and prior years",
        "lat": 49.2198, "lon": -122.9960,
        "phone": "604-299-5844",
        "website": "https://www.canadahelps.org/en/charities/burnaby-homeless-outreach-society/",
    },
    {
        "name": "AFCA BC Tax Clinic – Our Lady of Mercy Parish",
        "address": "7455 Tenth Ave, New Westminster, BC",
        "distance": "12.0 km",
        "type": "Walk-in",
        "languages": "English, Tagalog",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2010, "lon": -122.9120,
        "phone": "604-521-1671",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "Comptoir d'impôts CIIA / CAIA Tax Clinic",
        "address": "720 Twelfth St, New Westminster, BC",
        "distance": "13.1 km",
        "type": "Walk-in",
        "languages": "English, French, Kiswahili",
        "clientele": "Newcomers, Seniors, Students, Youth",
        "returns": "Current and prior years",
        "lat": 49.2102, "lon": -122.9236,
        "phone": "604-522-2495",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "Holy Eucharist Cathedral",
        "address": "501 Fourth Ave, New Westminster, BC",
        "distance": "13.9 km",
        "type": "By appointment",
        "languages": "English",
        "clientele": "Housing insecure, Indigenous, Newcomers, Seniors, Women only",
        "returns": "Current and prior years",
        "lat": 49.2072, "lon": -122.9126,
        "phone": "604-521-1434",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "A One Tax Help",
        "address": "#410-15225 104 Ave, Surrey, BC",
        "distance": "20.9 km",
        "type": "Virtual",
        "languages": "English, Cantonese, Mandarin, Punjabi",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.1876, "lon": -122.7765,
        "phone": "604-951-6400",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "Surrey Urban Mission Society",
        "address": "10776 King George Blvd, Surrey, BC",
        "distance": "14.8 km",
        "type": "Virtual",
        "languages": "English, French, Arabic, Hindi, Punjabi, Spanish, Turkish, Ukrainian",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.1882, "lon": -122.8448,
        "phone": "604-951-9900",
        "website": "https://surreymission.com/",
    },
    {
        "name": "Fraser Valley Taiwanese Society",
        "address": "8853 Selkirk St, Vancouver, BC",
        "distance": "28.1 km",
        "type": "Drop-off",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2288, "lon": -123.1060,
        "phone": "604-325-2474",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "Surrey Alliance Tax Service",
        "address": "13474 96 Ave, Surrey, BC",
        "distance": "17.5 km",
        "type": "Virtual",
        "languages": "English, Mandarin",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.1693, "lon": -122.8307,
        "phone": "604-585-6500",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "Sources Newton Clinic",
        "address": "#102 – 13771 72A Ave, Surrey, BC",
        "distance": "20.4 km",
        "type": "Virtual",
        "languages": "English, Hindi, Malayalam",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.1427, "lon": -122.8310,
        "phone": "604-596-2405",
        "website": "https://www.sourcesbc.ca/",
    },
    {
        "name": "Semiahmoo Library",
        "address": "100-1815 152 St, Surrey, BC",
        "distance": "26.5 km",
        "type": "Walk-in",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.0566, "lon": -122.8210,
        "phone": "604-531-1711",
        "website": "https://www.surreylibraries.ca/",
    },
    {
        "name": "Sources Women's Place",
        "address": "15318 20 Ave, Surrey, BC",
        "distance": "27.2 km",
        "type": "Drop-off",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.0521, "lon": -122.8024,
        "phone": "604-538-0459",
        "website": "https://www.sourcesbc.ca/",
    },
    {
        "name": "Sources Community Resources Food Bank",
        "address": "2343 156 St, Surrey, BC",
        "distance": "26.9 km",
        "type": "Drop-off",
        "languages": "English",
        "clientele": "Women only",
        "returns": "Current and prior years",
        "lat": 49.0490, "lon": -122.7975,
        "phone": "604-538-0596",
        "website": "https://www.sourcesbc.ca/",
    },
    {
        "name": "Peace Portal Tax Clinic",
        "address": "15128 27B Ave, Surrey, BC",
        "distance": "27.5 km",
        "type": "Drop-off",
        "languages": "English, Punjabi, Spanish",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.0591, "lon": -122.8068,
        "phone": "604-538-9516",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "First United Tax Clinic",
        "address": "320 Powell St, Vancouver, BC",
        "distance": "28.3 km",
        "type": "Walk-in",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2820, "lon": -123.0975,
        "phone": "604-681-8365",
        "website": "https://www.firstunited.ca/",
    },
    {
        "name": "Chinese Community Library Services",
        "address": "577 Pender St E, Vancouver, BC",
        "distance": "28.5 km",
        "type": "Walk-in",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2795, "lon": -123.0946,
        "phone": "604-251-4119",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
    {
        "name": "UBC Tax Assistance Clinic",
        "address": "6138 Student Union Blvd, Vancouver, BC",
        "distance": "37.2 km",
        "type": "Drop-off",
        "languages": "English",
        "clientele": "Persons with disabilities",
        "returns": "Current and prior years",
        "lat": 49.2660, "lon": -123.2496,
        "phone": "604-827-4567",
        "website": "https://allard.ubc.ca/pro-bono-students-canada",
    },
    {
        "name": "Disability Alliance BC",
        "address": "1450-605 Robson St, Vancouver, BC",
        "distance": "29.8 km",
        "type": "Walk-in",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.2818, "lon": -123.1205,
        "phone": "604-872-1278",
        "website": "https://disabilityalliancebc.org/",
    },
    {
        "name": "Malayalee Association (MACS)",
        "address": "14863-148A 63 Ave, Surrey, BC",
        "distance": "22.8 km",
        "type": "Virtual",
        "languages": "English",
        "clientele": "General public",
        "returns": "Current and prior years",
        "lat": 49.1001, "lon": -122.8150,
        "phone": "604-589-4111",
        "website": "https://www.canada.ca/en/revenue-agency/services/tax/individuals/community-volunteer-income-tax-program.html",
    },
]

# ── Colour map for clinic types ───────────────────────────────────────────────
TYPE_COLORS = {
    "Walk-in":        "#2a7d4f",
    "By appointment": "#c17d11",
    "Drop-off":       "#1a5f9e",
    "Virtual":        "#8b4db8",
}

def make_icon(color):
    return folium.DivIcon(html=f"""
        <div style="
            width:16px;height:16px;border-radius:50%;
            background:{color};
            border:2.5px solid white;
            box-shadow:0 1px 5px rgba(0,0,0,0.4);
        "></div>""",
        icon_size=(16, 16),
        icon_anchor=(8, 8),
    )

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:#1a3a4a;padding:0.5rem 0 0.2rem;">
        🍁 Tax Clinic Finder
    </div>
    <div style="font-size:0.8rem;color:#666;margin-bottom:1.2rem;">Burnaby & Surrounding Area · 2026</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-card"><h4>Filter by Type</h4>', unsafe_allow_html=True)
    selected_types = []
    for t, c in TYPE_COLORS.items():
        if st.checkbox(t, value=True, key=t):
            selected_types.append(t)
    st.markdown('</div>', unsafe_allow_html=True)

    max_dist = st.slider("Max distance (km)", 0, 40, 40)

    st.markdown('<div class="legend-box"><h4>Clinic Types</h4>', unsafe_allow_html=True)
    for t, c in TYPE_COLORS.items():
        st.markdown(f"""
        <div class="legend-item">
            <div class="dot" style="background:{c};"></div>
            <span>{t}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.2rem;font-size:0.75rem;color:#999;line-height:1.5;">
        Data sourced from CRA Community Volunteer Income Tax Program (CVITP). 
        Phone numbers are approximate — confirm availability before visiting.
    </div>""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>Free Tax Clinics</h1>
    <p>Burnaby, BC and surrounding communities · Volunteer-prepared returns · No charge</p>
</div>
""", unsafe_allow_html=True)

# ── Filter clinics ────────────────────────────────────────────────────────────
filtered = [
    c for c in clinics
    if c["type"] in selected_types
    and float(c["distance"].replace(" km", "")) <= max_dist
]

col_count, col_cra = st.columns([2, 3])
with col_count:
    st.markdown(f"""
    <div class="clinic-count">
        Showing <strong>{len(filtered)}</strong> of {len(clinics)} clinics
    </div>""", unsafe_allow_html=True)
with col_cra:
    st.info("💡 All clinics are part of the CRA's free CVITP program for modest-income Canadians.", icon=None)

# ── Build Folium map ──────────────────────────────────────────────────────────
m = folium.Map(
    location=[49.230, -122.980],
    zoom_start=11,
    tiles="CartoDB Positron",
)

for c in filtered:
    popup_html = f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;width:260px;padding:4px 2px;">
        <div style="font-size:14px;font-weight:700;color:#1a3a4a;margin-bottom:6px;line-height:1.3;">
            {c['name']}
        </div>
        <div style="font-size:12px;color:#555;margin-bottom:8px;">📍 {c['address']}</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;">
            <span style="background:{TYPE_COLORS[c['type']]};color:white;
                border-radius:99px;padding:2px 10px;font-size:11px;font-weight:600;">
                {c['type']}
            </span>
            <span style="background:#f0ece4;color:#444;
                border-radius:99px;padding:2px 10px;font-size:11px;">
                📏 {c['distance']}
            </span>
        </div>
        <table style="font-size:11.5px;color:#333;border-collapse:collapse;width:100%;">
            <tr><td style="padding:2px 0;color:#888;white-space:nowrap;padding-right:6px;">🌐 Languages</td>
                <td>{c['languages']}</td></tr>
            <tr><td style="padding:2px 0;color:#888;white-space:nowrap;padding-right:6px;">👥 Clientele</td>
                <td>{c['clientele']}</td></tr>
            <tr><td style="padding:2px 0;color:#888;white-space:nowrap;padding-right:6px;">📋 Returns</td>
                <td>{c['returns']}</td></tr>
        </table>
        <hr style="border:none;border-top:1px solid #e8e0d4;margin:8px 0;">
        <div style="font-size:12px;">
            📞 <a href="tel:{c['phone']}" style="color:#1a3a4a;text-decoration:none;font-weight:600;">{c['phone']}</a>
        </div>
        <div style="margin-top:5px;">
            🌍 <a href="{c['website']}" target="_blank"
               style="color:#2a7d4f;font-size:12px;font-weight:600;text-decoration:none;">
               Visit Website ↗
            </a>
        </div>
    </div>
    """
    folium.Marker(
        location=[c["lat"], c["lon"]],
        popup=folium.Popup(popup_html, max_width=290),
        tooltip=f"<b>{c['name']}</b><br><small>{c['type']} · {c['distance']}</small>",
        icon=make_icon(TYPE_COLORS[c["type"]]),
    ).add_to(m)



# ── Data table ────────────────────────────────────────────────────────────────
with st.expander("📋 View all clinics as a table"):
    import pandas as pd
    df = pd.DataFrame([{
        "Clinic": c["name"],
        "Address": c["address"],
        "Distance": c["distance"],
        "Type": c["type"],
        "Languages": c["languages"],
        "Clientele": c["clientele"],
        "Phone": c["phone"],
        "Website": c["website"],
    } for c in filtered])
    st.dataframe(df, use_container_width=True, hide_index=True)
