## CONFIGURATION OF DASH APP
apres avoir installer les differentes librairies, copier le code 
ci-dessous et remplacer celui a la ligne *74* jusqu'a *105* du fichier dash.py.
Pour l'ouvrir faite un *CTRL + CLICK* dessus apres l'import.

# code a remplcer

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
    <div class="text-center mt-100 text-primary">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden"></span>
        </div>
        Chargement...
    </div>
</div>
"""