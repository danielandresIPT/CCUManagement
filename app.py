import streamlit as st
import pandas as pd
import os

# Define the CSV file where data will be persisted
DATA_FILE = "data.csv"

# Load data from CSV or initialize with default values if file doesn't exist
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict(orient="records")
    else:
        # Default data with 5 rows, saved initially to CSV
        default_data = [
            {"CCU": "BR Compacta", "Descripción": "BR OPAL", "Dirección IP": "172.19.1.141", "Disponible": "No", "FW": "BZ0021(PT0110)", "Restablecer FW": "No", "Última modificación": "DAM"},
            {"CCU": "BR Compacta", "Descripción": "BR dSPACE", "Dirección IP": "172.19.1.139", "Disponible": "No", "FW": "BZ0021(PT0110)", "Restablecer FW": "No", "Última modificación": "DAM"},
            {"CCU": "BR Distribuida", "Descripción": "BR Dist. OPAL", "Dirección IP": "172.19.1.142", "Disponible": "Si", "FW": "BZ0009(PT0159)", "Restablecer FW": "No", "Última modificación": "DAM"},
            {"CCU": "AR", "Descripción": "AR OPAL", "Dirección IP": "172.19.1.140", "Disponible": "Si", "FW": "AZ3985(PT0204)", "Restablecer FW": "No", "Última modificación": "DAM"},
            {"CCU": "AR", "Descripción": "AR oficina", "Dirección IP": "172.19.1.22", "Disponible": "Si", "FW": "AZ2004(PT0085)", "Restablecer FW": "No", "Última modificación": "DAM"},
        ]
        df = pd.DataFrame(default_data)
        df.to_csv(DATA_FILE, index=False)
        return default_data

# Save the data to a CSV file
def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)

# Function to color the "Disponible" column
def color_available(val):
    color = '#DBF1D8' if val == 'Si' else '#F1D8D8'
    return f'background-color: {color}'

# Main application
def main():
    st.set_page_config(layout="wide")  # Use wide layout
    
    # CSS to style the header, footer, and reduce top margin
    st.markdown("""
        <style>
            /* Hide Streamlit header and footer */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Reduce top margin */
            .block-container {
                padding-top: 1rem;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Gestión de CCUs Sarriguren")

    # Check if the user's name is already in session state
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = ''

    # If the user has not entered their name, show the login page
    if not st.session_state['user_name']:
        st.subheader("Introduce tus iniciales para continuar")
        user_name = st.text_input("Iniciales")
        if st.button("Continuar"):
            st.session_state['user_name'] = user_name
            st.rerun()
    else:
        # Load the current data into session state if not already loaded
        if 'data' not in st.session_state:
            st.session_state['data'] = load_data()

        # Convert session state data to DataFrame
        df = pd.DataFrame(st.session_state['data'])

        # Apply color formatting to the "Disponible" column
        df_styled = df.style.applymap(color_available, subset=['Disponible'])

        # Overview Table (Now placed at the top)
        st.table(df_styled)

        # Tabs for Editing Data
        tabs = st.tabs([f"{row['Descripción']}" for row in st.session_state['data']])
        # Loop through each tab for each row
        for i, row in enumerate(st.session_state['data']):
            with tabs[i]:
                st.write(f"Actualizar estado para {row['Descripción']}:")
                
                # Editable fields with unique keys for each widget
                ip_address = st.text_input("IP Address", value=row["Dirección IP"], key=f"ip_{i}")
                available = st.selectbox("Disponible", ["Si", "No"], index=0 if row["Disponible"] == "Si" else 1, key=f"available_{i}")
                fw = st.text_input("Firmware Version (FW)", value=row["FW"], key=f"fw_{i}")
                restore_fw = st.selectbox("Restablecer FW", ["Si", "No"], index=0 if row["Restablecer FW"] == "Si" else 1, key=f"restore_fw_{i}")

                # Update the data when any field changes
                if st.button(f"Actualizar estado", key=f"save_{i}"):
                    st.session_state['data'][i]["Dirección IP"] = ip_address
                    st.session_state['data'][i]["Disponible"] = available
                    st.session_state['data'][i]["FW"] = fw
                    st.session_state['data'][i]["Restablecer FW"] = restore_fw
                    st.session_state['data'][i]["Última modificación"] = st.session_state['user_name']
                    save_data(st.session_state['data'])  # Save to CSV
                    st.success(f"Camnbios guardados para {row['Descripción']}.")
                    st.rerun()  # Reload the app to reflect changes in the table

if __name__ == "__main__":
    main()
