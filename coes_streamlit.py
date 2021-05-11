#LIBRERÍAS
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go


##############################################################################
#Webpage css colors: https://www.quackit.com/css/css_color_codes.cfm
#Emojis HTML: https://www.w3schools.com/charsets/ref_emoji.asp

#STREAMLIT CONTAINER CUSTOMIZE
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 1rem;
        padding-right: 4rem;
        padding-left: 4rem;
        padding-bottom: 4rem;
    }}
    img{{
    	max-width:100%;
    	margin-bottom:10px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
#BOTON 'OBTENER RESULTADOS' CUSTOMIZE
st.markdown(f"""
	<style>.css-qbe2hs {{
	    display: inline-flex;
	    -webkit-box-align: center;
	    align-items: center;
	    -webkit-box-pack: center;
	    justify-content: center;
	    font-weight: 600;
	    padding: 0.25rem 0.75rem;
	    border-radius: 0.75rem;
	    margin: 0px;
	    line-height: 3;
	    color: #FFFFFF;
	    width: auto;
	    background-color: rgba(0,102,204, 0.8);
	    border: 2px solid rgba(38, 39, 48, 0.9);}}
	</style>
	""",unsafe_allow_html=True,)

#TITULO APP CUSTOMIZE
st.subheader('¡Bienvenido! :earth_americas: :sunny: :wind_blowing_face:')
Title_html = """
	<style>
		.wrapper h1{
		  height: 100vh;
		  /*This part is important for centering*/
		  display: flex;
		  align-items: center;
		  justify-content: center;
		}
		.typing-demo {
		  width: 14ch;
		  animation: typing 3s steps(60), blink .5s step-end infinite alternate;
		  white-space: nowrap;
		  overflow: hidden;
		  border-right: 3px solid;
		  font-family: cursive;
		  font-size: 3em;
		  font-weight: 550;
		  color: #0066cc;
		}
		@keyframes typing {
		  from {
		    width: 0
		  }
		}
		@keyframes blink {
		  50% {
		    border-color: transparent
		  }
		}
	</style>
	<div class="wrapper">
	    <div class="typing-demo">
	      RenewablesAPP.🇵🇪
	    </div>
	</div>
	"""
st.markdown(Title_html, unsafe_allow_html=True) #Title rendering


##############################################################################
#CONTAINERS
header_container = st.beta_container()
data_container = st.beta_container()
user_container = st.beta_container()
table_container = st.beta_container()
graph_container = st.beta_container()

#######################################
with header_container:
#CABECERA
	st.write('Aplicación web (en fase βeta) para mostrar data relevante de las centrales eólicas y solares en el Perú')
	st.image('images/renewables.jpeg', width=600, caption='Energía limpia para un futuro energético sostenible')
	st.write('')

#######################################
with data_container:
#CARGANDO DATOS DESDE .CSV
	
	@st.cache
	def load_coes_data():
		df = pd.read_csv('data/databasecoesrer.csv', parse_dates=[0], index_col=0, dayfirst=1)
		return df

	data_total = load_coes_data()

	# #PRUEBA CONVERTIR FORMATO DATE!!!!
	# data_total.reset_index(inplace=True)
	# st.write(data_total.head())

	# data_total['Fecha'] = pd.to_datetime(data_total['Fecha']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')
	# data_total['Fecha'] = pd.to_datetime(data_total['Fecha'])
	# data_total.set_index("Fecha", inplace = True)
	# st.write(type(data_total.index))
	# st.write(data_total.head())

	data_empty = pd.DataFrame(columns=data_total.columns) #Para la tabla por defecto
	data_selected = data_empty

	#st.write(data_total.style.apply())

	# data_total.format(formatter=lambda x: x.strftime('%Y:%m:%d %H:%M'))
#######################################
	def header(url):
	     st.markdown(f'<p style="background-color:#0066cc;color:#FFFFFF;font-size:20px; font-weight:500;">{url}</p>', unsafe_allow_html=True)

	header('1. Seleccione el tipo de tecnología renovable y un rango de fechas')

with user_container:

	st.write('Ingresa tus requerimientos en los siguientes campos y dar click al botón: ⚡GO RER⚡')

	col1, col2 =st.beta_columns(2)

#SELECTCBOX: SELECCIONAR TIPO DE TECNOLOGÍA

	col1.subheader('1.1. Tipo de tecnología renovable')

	chart_visual = col1.selectbox('Seleccione el tipo de tecnología o una central RER individual:', 
		('<Seleccione un opción>', 'Central RER individual', 'Centrales eólicas', 'Centrales solares', 
		'Centrales solares y centrales eólicas (ambas)'))

	count = 1
	checker = False
	if chart_visual == 'Central RER individual':
		chart_visual = col1.selectbox('Escoja la central renovable:', ['<Seleccione un opción>'] + data_total.columns.tolist())
		if chart_visual == '<Seleccione un opción>':
			col1.warning("Por favor, seleccione una central renovable.")
		for i in data_total.columns:
			if chart_visual == i:
				data_selected = data_total.copy()[i]
				col1.success("¡Correcto!:heavy_check_mark:")
				checker = True

	elif chart_visual == 'Centrales eólicas':
		data_selected = data_total.copy().iloc[:, :7]
		for i in data_selected.columns:
			col1.text('{0}. {1}'.format(count, i))
			count+=1
		col1.success("¡Correcto!:heavy_check_mark:")
		checker = True

	elif chart_visual == 'Centrales solares':
		data_selected = data_total.copy().iloc[:, 7:]
		for i in data_selected.columns:
			col1.text('{0}. {1}'.format(count, i))
			count+=1
		col1.success("¡Correcto!:heavy_check_mark:")
		checker = True

	elif chart_visual == 'Centrales solares y centrales eólicas (ambas)':
		data_selected = data_total.copy()
		for i in data_selected.columns:
			col1.text('{0}. {1}'.format(count, i))
			count+=1
		col1.success("¡Correcto!:heavy_check_mark:")
		checker = True

	elif chart_visual == '<Seleccione un opción>':
		col1.warning("Por favor, seleccione el 'tipo de tecnología'")
		checker = False


#CALENDARIO: SELECCIONAR RANGO DE FECHAS
	start_date = '2011-1-2' #start_date declarado arbitrariamente para no lanzar error en el calendario.
	end_date = '2011-1-1' #end_date declarado arbitrariamente para no lanzar error en el calendario

	col2.subheader("1.2 Rango de fechas")
	try:
		start_date, end_date = col2.date_input('Seleccione una fecha inicial y una fecha final:', 
			value=(datetime.datetime(2020, 12, 31), datetime.datetime(2020, 12, 31)),
			min_value=datetime.datetime(2012, 7, 6), max_value=datetime.datetime.now())
		
		if start_date<end_date:
			col2.success("¡Correcto!:heavy_check_mark:")
		else:
			col2.warning('Por favor, selecciona una fecha mayor que la otra.')

	except:
		col2.warning('Por favor, selecciona ambas fechas: inicial y final')


	data_user_date = data_selected.loc[start_date:end_date]


#BOTÓN GENERAL: OBTENER RESULTADOS
	st.text('')
	col3, col4, col5 =st.beta_columns([1.48,1,1])
	press_button = col4.button("⚡ GO RER ⚡", key='press_button')


#######################################

with table_container:
	header("2. Resultados")

	#TABLA DE DATOS VACIO POR DEFECTO
	def table_empty():
		st.dataframe(data_empty)

	#GRÁFICO VACIO POR DEFECTO
	def graph_empty(arg): #Argumento debe ser un dataframe
		fig = px.line(arg)
		fig.update_layout(
			title="Potencia generada por la central renovable",
			xaxis_title="Fecha",
			yaxis_title="Potencia [MW]",
			legend_title="Central renovable:",
			)
		st.plotly_chart(fig, use_container_width=True)

	#REPETIR TABLA Y GRAFICO VACIOS
	def repeat():
		st.subheader('2.1 Tabla de datos por defecto (vacío):')
		table_empty()
		st.subheader('2.2 Gráfico por defecto (vacío):')
		graph_empty(None)


	#TABLA DE DATOS Y GRAFICOS
	try:
		if press_button==True and start_date<end_date and checker==True:
			st.subheader('2.1 Tabla de datos (fechas seleccionadas):')
			st.dataframe(data_user_date)
			st.subheader('3.1 Gráfico (fechas seleccionadas):')
			graph_empty(data_user_date)

		elif press_button==True and start_date>=end_date and checker==False:
			st.error("Error: Por favor, seleccione correctamente el 'tipo de tecnología' y el 'rango de fechas'.")
			repeat()

		elif press_button==True and start_date<end_date and checker==False:
			st.error("Error: Por favor, seleccione correctamente el 'tipo de tecnología'.")
			repeat()

		elif press_button==True and start_date>=end_date and checker==True:
			st.error("Error: Por favor, seleccione correctamente el 'rango de fechas'.")
			repeat()

		else:
			repeat()

	except:
			pass
