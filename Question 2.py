import os
import pandas as pd
import plotly.graph_objects as go

# Makes df
df = pd.DataFrame(columns=['Sample', 'Total Breaks'])

# Questions 2a-b

# Reads all files in the output dir and adds their total breaks to the df
for subdir, dirs, files in os.walk('output'):
    for f in files:
        filepath = subdir + os.sep + f
        data = pd.read_csv(filepath, sep='\t')
        data.columns = ['Chromosome', 'Start', 'Stop', 'Number of Breaks']
        row = {'Sample': f, 'Total Breaks': data['Number of Breaks'].sum()}
        new_df = pd.DataFrame([row])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)


# Question 2c

# Normalises the asiSl Breaks
for subdir, dirs, files in os.walk('tmp/intervals/adjustedintervals'):
    tmp = []
    for f in files:
        filepath = subdir + os.sep + f
        data = pd.read_csv(filepath, sep='\t')
        breaks = len(data.index)
        normalisedbreaks = breaks/1000
        tmp.append(normalisedbreaks)
df['NBreaks'] = tmp
df['Normalised Breaks'] = df['Total Breaks']/df['NBreaks']
df = df.drop(columns=['NBreaks'])

# Question 2d

# Creates the graph
fig = go.Figure()

# Adds the number of breaks to the graph
fig.add_trace(go.Scatter(x=df['Total Breaks'],
                         y=df['Sample'],
                         name='Total Number of Breaks',
                         marker_symbol=1,
                         marker=dict(
                            color='rgba(156, 165, 196, 0.95)',
                            line_color='rgba(156, 165, 196, 1.0)')
                        ))

# Adds the Normalised Breaks to the graph
fig.add_trace(go.Scatter(x=df['Normalised Breaks'],
                         y=df['Sample'],
                         name='Normalised Number of Breaks',
                         marker_symbol=2,
                         marker=dict(
                            color='rgba(204, 204, 204, 0.95)',
                            line_color='rgba(217, 217, 217, 1.0)')
                        ))

# Updates figure Layout
fig.update_traces(mode='markers', marker=dict(line_width=1, size=16))

fig.update_layout(
    title="Number of AsiSl Breaks in Each Sample",
    xaxis=dict(
        title='Count',
        showgrid=False,
        showline=True,
        linecolor='rgb(102, 102, 102)',
        tickfont_color='rgb(102, 102, 102)',
        showticklabels=True,
        dtick=10,
        ticks='outside',
        tickcolor='rgb(102, 102, 102)',
    ),
    margin=dict(l=140, r=40, b=50, t=80),
    legend=dict(
        font_size=10,
        yanchor='middle',
        xanchor='right',
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    hovermode='closest',
)
fig.show()
