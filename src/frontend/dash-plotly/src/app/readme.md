## APP CONFIGURATIONS

jump inside dash library and update the following line started from 75 to 104
with the following code

_default_index = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <!--[if IE]><script>
        alert("Dash v2.7+ does not support Internet Explorer. Please use a newer browser.");
        </script><![endif]-->
        {%app_entry%}
        <footer class="d-none">
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

_app_entry = """
<div id="react-entry-point">
    <div class="_dash-loading text-center mt-100 text-primary">
        <div class="spinner-border" role="status">
            <span class="visually-hidden"></span>
        </div>
    </div>
</div>
"""