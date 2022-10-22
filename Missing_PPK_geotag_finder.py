from geopy import distance
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

# inputs
print('\n****** BUSCADOR DE ERRORES EN GEOTAGS - PPK ******')
file_name = input('\nIngrese nombre del archivo: ')
image_start = int(input('Ingrese número de la primera imagen: '))

# open file
file = open(f'{file_name}')

# read file
content = file.readlines()

# list with latitude coordinates
lat = []
for i in content:
    if i.startswith('2'):
        lat.append(float(i[25:38]))

# list with longitude coordinates
lon = []
for i in content:
    if i.startswith('2'):
        lon.append(float(i[40:53]))
file.close()

# list with all distance between consecutive points
distances = []
for i in range(len(lat)-1):
    if i != len(lat):
        distances.append(distance.distance((lat[i], lon[i]), (lat[i+1], lon[i+1])).m)
    else:
        pass

# start of gaps indexes
index_start_gap = []
# average
suma = 0
for i in distances:
    suma += i
average = suma/len(distances)

for i in range(len(distances)-1):
    if distances[i+1] > average * 1.5:
        index_start_gap.append(i)

# indexes to delete and list with indexes per hole
add = 0
indexes_to_delete = []
indexes_to_delete_holes = []
for i in index_start_gap:
    indexes_to_delete_holes.append([])
counter = 0
for i in index_start_gap:
    # number of images in the gap
    images_to_add = (round(distances[i+1]/average))-1

    for n in range(1, images_to_add+1):
        indexes_to_delete.append(add + i + n)
        indexes_to_delete_holes[counter].append(add + i + n)
    counter += 1
    add += images_to_add

# total number of images taken
total_length = len(lat) + len(indexes_to_delete)

# indexes of coordinates recorded by gps
indexes_recorded = []
for i in range(total_length):
    if i-1 not in indexes_to_delete:
        indexes_recorded.append(i)
    else:
        pass

# number of images recoded by gps
images_recorded = [i + image_start for i in indexes_recorded]

# number of images not recorded by gps
images_not_recorded = [i + image_start+1 for i in indexes_to_delete]

# output text (images to delete from dataset)
text_images_output = ''
for i in images_not_recorded:
    text_images_output += str(i) + '  '


# center of gaps
center_gaps_lat = []
center_gaps_lon = []

for i in index_start_gap:
    center_gaps_lat.append((lat[i+1] + lat[i+2]) / 2)
    center_gaps_lon.append((lon[i+1] + lon[i+2]) / 2)


# dataframe with lat, lon and image numbers
df = pd.DataFrame({'latitud': lat,
                   'longitud': lon,
                   'imagen': images_recorded})


# function to add holes to plot. Arguments figure and size
def add_holes(fig, size_):
    fig.add_trace(go.Scatter(
        mode='markers',
        x=center_gaps_lon,
        y=center_gaps_lat,
        marker=dict(color='rgba(255, 0, 0, 0.2)', size=size_, line=dict(color='Red', width=2)),
        showlegend=False))
    fig.update_xaxes(title='Longitud', visible=True, showticklabels=False)
    fig.update_yaxes(title='Latitud', visible=True, showticklabels=False)


text_01 = ''
if len(images_not_recorded) == 0:
    text_01 = 'El vuelo está OK. No se encontraron huecos.'
elif len(images_not_recorded) == 1:
    text_01 = f'Se encontró {len(index_start_gap)} hueco.'
else:
    text_01 = f'Se encontraron {len(index_start_gap)} huecos.'
# Create figure 1
fig = px.scatter(df, x=lon, y=lat, title=f'{text_01}\nLa primera imagen del vuelo es la nº {image_start} y la última es la nº {image_start + len(images_recorded) + len(images_not_recorded) - 1} ')

# add holes to fig 1 with size 30
add_holes(fig, 30)

print(f'\nSe encontraron {len(index_start_gap)} huecos.')
# Show figure 2
fig.show()

# Create figure 2
fig2 = go.Figure(
    data=go.Scatter(
            x=df['longitud'],
            y=df['latitud'],
            text=df['imagen'],
            textposition='top right',
            textfont=dict(color='#E58606'),
            mode='lines+markers+text',
            marker=dict(color='#5D69B1', size=8),
            line=dict(color='#52BCA3', width=1, dash='dash')),
    layout=dict(
            title=f'Las imágenes sin geotag son: {text_images_output}',
            xaxis=dict(title='Longitud',
                        linecolor='#d9d9d9',),
            yaxis=dict(title='Latitud',
                         linecolor='#d9d9d9',)))

# add holes to fig 2 with size 50
add_holes(fig2, 50)

print(f'Las imágenes sin geotag son: {text_images_output}')

# Show figure 2
fig2.show()