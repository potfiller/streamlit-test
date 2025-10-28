import altair as alt
from vega_datasets import data

source = data.seattle_weather()

select = alt.selection_point(name="select", on="click")
highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)

stroke_width = (
    alt.when(select).then(alt.value(2, empty=False))
    .when(highlight).then(alt.value(1))
    .otherwise(alt.value(0))
)

alt.Chart(source).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3,
    stroke="black", cursor="pointer"
).encode(
    x='month(date):O',
    y='count():Q',
    tooltip=['month(date):O', 'count():Q'],
    color='weather:N',
    fillOpacity=alt.when(select).then(alt.value(1)).otherwise(alt.value(0.3)),
    strokeWidth=stroke_width,
).configure_scale(
    bandPaddingInner=0.2
).add_params(
    select, 
    highlight
).save(
    'test.html'
)