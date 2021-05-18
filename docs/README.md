
{! README.md !}


## Setup

Initialize a `CORHEL_Kamodo` object by pointing to a run directory and subdirectory containing MAS variables.

```python
from corhel import CORHEL_Kamodo
```

```python
cor = CORHEL_Kamodo('/home/data/areyes_at_predsci.com_20210319_1_zb', mhd_path='cme/mhd')
```

When viewed in a Jupyter notebook, the `CORHEL_Kamodo` instance appears as a set of field signatures.


$$ f(x) $$

```python
cor
```

```python
from IPython.core.display import display, HTML
display(HTML(cor.to_latex(mode='equation')))
```

## Slice interpolation

By default, the above functions are registered as slice interpolators. This allows us to generate slices by fixing one of the coordinates: 

```python
cor.v_r(r=1.5).shape
```

The above shape of the returned array matches the local resolution of the model.
To plot the above data, we can rely on Kamodo's default plotting behavior for functions matching this signature.

```python
help(cor.plot)
```

```python
fig = cor.plot(v_r={'r':1.5})
fig
```

```python
from plotly.offline import plot

from kamodo.cli.main import write_plot_div

write_plot_div(plot(fig, output_type='div', include_mathjax='cdn', include_plotlyjs='cdn'), 'fig1.html')
```

{! docs/fig1.html !}



```python

```
