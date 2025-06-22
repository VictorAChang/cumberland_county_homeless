import streamlit as st
import folium
from streamlit_folium import st_folium

# ----------------- Page Configuration -----------------
st.set_page_config(page_title="Fayetteville Homeless Map", layout="wide")

# Custom header with style
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    /* Darker sidebar background */
    [data-testid="stSidebar"] {
        background-color: #e0e0e0 !important;
    }

    /* Optional: sidebar text color and padding */
    .css-ng1t4o {
        color: #000000 !important;
        padding: 1rem;
    }
    </style>
    <div class="main-title">🗺️ Fayetteville Homeless Resources & Concentrations Map</div>
""", unsafe_allow_html=True)

# ----------------- Resource Data -----------------
locations = [
    # Homeless
    {"Name": "Bus Station", "Address": "505 Franklin St", "Lat": 35.0566, "Lon": -78.8795, "People": 80, "Category": "Homeless"},
    {"Name": "Gillespie Zone", "Address": "702 Gillespie St", "Lat": 35.0364, "Lon": -78.8802, "People": 25, "Category": "Homeless"},
    {"Name": "Camp Maria", "Address": "335 Ray Ave", "Lat": 35.0580, "Lon": -78.8843, "People": 15, "Category": "Homeless"},
    {"Name": "Dollar Tree Raeford", "Address": "7715 S Raeford Rd", "Lat": 35.0225, "Lon": -79.0267, "People": 10, "Category": "Homeless"},
    {"Name": "B Street", "Address": "519 Grove St", "Lat": 35.0588, "Lon": -78.8739, "People": 25, "Category": "Homeless"},
    {"Name": "Public Library", "Address": "300 Maiden Ln", "Lat": 35.0569, "Lon": -78.8809, "People": 80, "Category": "Homeless"},

    # Shelters
    {"Name": "True Vine Ministries (J Center)", "Address": "5315 Morganton Rd", "Lat": 35.0720, "Lon": -78.9845, "Category": "Shelter"},
    {"Name": "Cornerstone Empowerment Center", "Address": "111 N. Bragg Blvd", "Lat": 35.3110, "Lon": -78.9755, "Category": "Shelter"},
    {"Name": "The Salvation Army", "Address": "245 Alexander St", "Lat": 35.0546, "Lon": -78.8769, "Category": "Shelter"},
    {"Name": "CIHN Family Shelter", "Address": "Fayetteville, NC", "Lat": 35.0625, "Lon": -78.8730, "Category": "Shelter", "Details": "Emergency shelter for homeless children & families."},
    {"Name": "Connections Day Resource", "Address": "119 N Cool Spring St", "Lat": 35.0521, "Lon": -78.8663, "Category": "Shelter", "Details": "Day resource & case mgmt for women & children."},

    # Warming Centers
    {"Name": "DSS Auxiliary Lobby", "Address": "1225 Ramsey St", "Lat": 35.0838, "Lon": -78.8807, "Category": "Warming Center"},
    {"Name": "Public Health Lobby", "Address": "1235 Ramsey St", "Lat": 35.0847, "Lon": -78.8808, "Category": "Warming Center"},
    {"Name": "FAST Lobby", "Address": "505 Franklin St", "Lat": 35.0566, "Lon": -78.8795, "Category": "Warming Center"},
    {"Name": "Fayetteville Cares Day Center", "Address": "128 South King St", "Lat": 35.0534, "Lon": -78.8781, "Category": "Warming Center"},

    # Health Centers
    {"Name": "Stedman-Wade Health Services", "Address": "7118 Main St, Wade, NC 28395", "Lat": 35.1403, "Lon": -78.7377, "Category": "Health Center", "Details": "Primary care, behavioral health, dental"},
    {"Name": "CommWell Health - Newton Grove", "Address": "306 Beaman St, Clinton, NC 28328", "Lat": 35.1935, "Lon": -78.3737, "Category": "Health Center", "Details": "Sliding scale, mental health, pediatrics"},
    {"Name": "Cumberland County Department of Public Health", "Address": "1235 Ramsey St", "Lat": 35.0846, "Lon": -78.8806, "Category": "Health Center", "Details": "STD testing, immunizations, family planning"},
    {"Name": "Fayetteville VA Medical Center", "Address": "2300 Ramsey St", "Lat": 35.0935, "Lon": -78.8717, "Category": "Health Center", "Details": "Veterans primary, mental healthcare, social work."},
    {"Name": "Employee Health Center", "Address": "1235 Ramsey St", "Lat": 35.0846, "Lon": -78.8808, "Category": "Health Center", "Details": "Acute & chronic care for county employees and dependents."},

    # Job Centers
    {"Name": "NCWorks Career Center", "Address": "414 Ray Ave", "Lat": 35.0562, "Lon": -78.8824, "Category": "Job Center", "Details": "Resume help, job placement, training"},
    {"Name": "Employment Source, Inc.", "Address": "600 Ames St", "Lat": 35.0647, "Lon": -78.8903, "Category": "Job Center", "Details": "Support for people with disabilities"},
    {"Name": "NCWorks Career Center (McPherson)", "Address": "490 N McPherson Church Rd", "Lat": 35.0590, "Lon": -78.8920,"Category": "Job Center", "Details": "Job search, resume help, skills training."},

    # Libraries
    {"Name": "Headquarters Library", "Address": "300 Maiden Ln", "Lat": 35.0573, "Lon": -78.8812, "Category": "Library", "Details": "Public computers, job help, events"},
    {"Name": "Cliffdale Regional Library", "Address": "6882 Cliffdale Rd", "Lat": 35.0529, "Lon": -79.0254, "Category": "Library", "Details": "Free Wi-Fi, youth programs"},
]

# ----------------- Styling -----------------
category_styles = {
    "Homeless": {"color": "#e74c3c"},
    "Shelter": {"color": "#3498db"},
    "Warming Center": {"color": "#2ecc71"},
    "Health Center": {"color": "#f39c12"},
    "Job Center": {"color": "#9b59b6"},
    "Library": {"color": "#1abc9c"},
}

st.toast("👉 Use the sidebar to filter resources.", icon="✨")

# Sidebar Filters
st.sidebar.title("📌 Filter Categories")
st.sidebar.markdown("### Select resource types:")
selected_categories = []
for category in category_styles:
    if st.sidebar.checkbox(category, value=True):
        selected_categories.append(category)

# ----------------- Folium Map -----------------
m = folium.Map(location=[35.05, -78.89], zoom_start=12, tiles="cartodbpositron")

for loc in [l for l in locations if l["Category"] in selected_categories]:
    style = category_styles[loc["Category"]]
    radius = loc.get("People", 10) / 2.5 if loc["Category"] == "Homeless" else 8
    popup_html = f"""
        <div style='font-size:14px;'>
        <b>{loc['Name']}</b><br>{loc['Address']}<br><b>{loc['Category']}</b>"""
    if "People" in loc:
        popup_html += f"<br>Estimated People: {loc['People']}"
    if "Details" in loc:
        popup_html += f"<br><i>{loc['Details']}</i>"
    popup_html += "</div>"

    folium.CircleMarker(
        location=[loc["Lat"], loc["Lon"]],
        radius=radius,
        color=style["color"],
        fill=True,
        fill_color=style["color"],
        fill_opacity=0.75,
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=loc["Name"]
    ).add_to(m)

# ----------------- Legend -----------------
legend_html = """
<div style="position: fixed; bottom: 20px; left: 20px; background:#ffffffdd; color:#222; padding:10px;
             border:2px solid #ccc; border-radius:8px; font-size:14px; box-shadow:2px 2px 6px #999; z-index:9999;">
<b>Legend</b><br>
<span style="color:#e74c3c;">●</span> Homeless<br>
<span style="color:#3498db;">●</span> Shelter<br>
<span style="color:#2ecc71;">●</span> Warming Center<br>
<span style="color:#f39c12;">●</span> Health Center<br>
<span style="color:#9b59b6;">●</span> Job Center<br>
<span style="color:#1abc9c;">●</span> Library
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ----------------- Render Map -----------------
st_folium(m, width=1000, height=620)
