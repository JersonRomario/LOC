import streamlit as st
from pathlib import Path
import zipfile
import shutil

def loc(directory):
    loc = 0
    lBlanco = 0
    comentarios = 0
    try:
        for path in Path(directory).rglob('.'):
            if not archivo(path):
                continue
            
            with path.open('r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    stripped_line = line.strip()
                    if not stripped_line:
                        lBlanco += 1
                    elif stripped_line.startswith(('#', '//', '/', '', '--', ';')):
                        comentarios += 1
                    else:
                        loc += 1
    except UnicodeDecodeError:
        st.warning(f"Error de codificación en el archivo: {path}")
        return 0, 0, 0
    
    return loc, lBlanco, comentarios

def archivo(file_path):
    text_file_extensions = ['.txt', '.js', '.py', '.java', '.cpp', '.html', '.css', '.php', '.rb', '.c', '.h', '.sql']
    return any(file_path.suffix.lower() == ext for ext in text_file_extensions)

def reporte(data):
    report = f"""Cuadro 1: Evaluación de métricas LOC del archivo 

- Líneas de Código (LOC): {data['loc']}
- Líneas Ejecutables (ELOC): {data['eloc']}
- Líneas de Comentarios (CLOC): {data['cloc']}
- Comment to Code Ratio (CCR): {data['ccr']:.2f}
- Líneas No Comentadas (NCLOC): {data['ncloc']}
- Líneas en Blanco (BLOC): {data['bloc']}

 """
    return report

def desReporte(report):
    with open('report.txt', 'w', encoding='utf-8') as file:
        file.write(report)
    return 'report.txt'

st.title('Calculadora de Métricas LOC')
st.write('Carga un archivo zip de un repositorio de GitHub para calcular las métricas LOC.')

uploaded_file = st.file_uploader('Sube un archivo zip', type='zip')

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall('temp_repo')

    loc, lBlanco, comentarios = loc('temp_repo')

    cloc = comentarios
    eloc = loc
    ncloc = cloc + eloc
    bloc = lBlanco

    if eloc > 0:
        ccr = cloc / eloc
    else:
        ccr = 0.0

    data = {
        'loc': loc,
        'eloc': eloc,
        'cloc': cloc,
        'ccr': ccr,
        'ncloc': ncloc,
        'bloc': bloc
    }

    st.write('Resultados:')
    st.write(f"- Líneas de Código (LOC): {loc}")
    st.write(f"- Líneas Ejecutables (ELOC): {eloc}")
    st.write(f"- Líneas de Comentarios (CLOC): {cloc}")
    st.write(f"- Comment to Code Ratio (CCR): {ccr:.2f}")
    st.write(f"- Líneas No Comentadas (NCLOC): {ncloc}")
    st.write(f"- Líneas en Blanco (BLOC): {bloc}")

    st.write('Descargar informe en formato TXT:')
    if st.button('Descargar Informe'):
        report = reporte(data)
        file_path = desReporte(report)
        st.markdown(f'Descarga [aquí]({file_path})', unsafe_allow_html=True)

    try:
        shutil.rmtree('temp_repo', ignore_errors=True)
    except Exception as e:
        st.error(f"No se pudo limpiar el directorio temporal: {e}")