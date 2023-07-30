dict_tpl = {'toc2.tpl': '{%- extends \'nbextensions.tpl\' -%}\n\n\n{%- block header -%}\n{{ super() }}\n\n <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.css">\n\n<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js"></script>\n\n<link rel="stylesheet" type="text/css" href="https://rawgit.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/main.css">\n\n<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">\n\n<script src="https://rawgit.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/toc2.js"></script>\n\n<script>\n$( document ).ready(function(){\n\n            var cfg = {{ nb.get(\'metadata\', {}).get(\'toc\', {})|tojson|safe }};\n\n            // fire the main function with these parameters\n            require([\'nbextensions/toc2/toc2\'], function (toc2) {\n                toc2.table_of_contents(cfg);\n            });\n    });\n</script>\n\n{%- endblock header -%}\n',
 'nbextensions.tpl': '{%- extends \'full.tpl\' -%}\n\n{% block input_group -%}\n{%- if cell.metadata.hide_input or nb.metadata.hide_input -%}\n{%- else -%}\n{{ super() }}\n{%- endif -%}\n{% endblock input_group %}\n\n{% block output_group -%}\n{%- if cell.metadata.hide_output -%}\n{%- else -%}\n    {{ super() }}\n{%- endif -%}\n{% endblock output_group %}\n\n{% block output_area_prompt %}\n{%- if cell.metadata.hide_input or nb.metadata.hide_input -%}\n    <div class="prompt"> </div>\n{%- else -%}\n    {{ super() }}\n{%- endif -%}\n{% endblock output_area_prompt %}\n',
 'basic.tpl': '{%- extends \'display_priority.j2\' -%}\n{% from \'celltags.tpl\' import celltags %}\n\n{% block codecell %}\n<div class="cell border-box-sizing code_cell rendered{{ celltags(cell) }}">\n{{ super() }}\n</div>\n{%- endblock codecell %}\n\n{% block input_group -%}\n<div class="input">\n{{ super() }}\n</div>\n{% endblock input_group %}\n\n{% block output_group %}\n<div class="output_wrapper">\n<div class="output">\n{{ super() }}\n</div>\n</div>\n{% endblock output_group %}\n\n{% block in_prompt -%}\n<div class="prompt input_prompt">\n    {%- if cell.execution_count is defined -%}\n        In&nbsp;[{{ cell.execution_count|replace(None, "&nbsp;") }}]:\n    {%- else -%}\n        In&nbsp;[&nbsp;]:\n    {%- endif -%}\n</div>\n{%- endblock in_prompt %}\n\n{% block empty_in_prompt -%}\n<div class="prompt input_prompt">\n</div>\n{%- endblock empty_in_prompt %}\n\n{# \n  output_prompt doesn\'t do anything in HTML,\n  because there is a prompt div in each output area (see output block)\n#}\n{% block output_prompt %}\n{% endblock output_prompt %}\n\n{% block input %}\n<div class="inner_cell">\n    <div class="input_area">\n{{ cell.source | highlight_code(metadata=cell.metadata) }}\n    </div>\n</div>\n{%- endblock input %}\n\n{% block output_area_prompt %}\n{%- if output.output_type == \'execute_result\' -%}\n    <div class="prompt output_prompt">\n    {%- if cell.execution_count is defined -%}\n        Out[{{ cell.execution_count|replace(None, "&nbsp;") }}]:\n    {%- else -%}\n        Out[&nbsp;]:\n    {%- endif -%}\n{%- else -%}\n    <div class="prompt">\n{%- endif -%}\n    </div>\n{% endblock output_area_prompt %}\n\n{% block output %}\n<div class="output_area">\n{% if resources.global_content_filter.include_output_prompt %}\n    {{ self.output_area_prompt() }}\n{% endif %}\n{{ super() }}\n</div>\n{% endblock output %}\n\n{% block markdowncell scoped %}\n<div class="cell border-box-sizing text_cell rendered{{ celltags(cell) }}">\n{%- if resources.global_content_filter.include_input_prompt-%}\n    {{ self.empty_in_prompt() }}\n{%- endif -%}\n<div class="inner_cell">\n<div class="text_cell_render border-box-sizing rendered_html">\n{{ cell.source  | markdown2html | strip_files_prefix }}\n</div>\n</div>\n</div>\n{%- endblock markdowncell %}\n\n{% block unknowncell scoped %}\nunknown type  {{ cell.type }}\n{% endblock unknowncell %}\n\n{% block execute_result -%}\n{%- set extra_class="output_execute_result" -%}\n{% block data_priority scoped %}\n{{ super() }}\n{% endblock data_priority %}\n{%- set extra_class="" -%}\n{%- endblock execute_result %}\n\n{% block stream_stdout -%}\n<div class="output_subarea output_stream output_stdout output_text">\n<pre>\n{{- output.text | ansi2html -}}\n</pre>\n</div>\n{%- endblock stream_stdout %}\n\n{% block stream_stderr -%}\n<div class="output_subarea output_stream output_stderr output_text">\n<pre>\n{{- output.text | ansi2html -}}\n</pre>\n</div>\n{%- endblock stream_stderr %}\n\n{% block data_svg scoped -%}\n<div class="output_svg output_subarea {{ extra_class }}">\n{%- if output.svg_filename %}\n<img src="{{ output.svg_filename | posix_path }}">\n{%- else %}\n{{ output.data[\'image/svg+xml\'] }}\n{%- endif %}\n</div>\n{%- endblock data_svg %}\n\n{% block data_html scoped -%}\n<div class="output_html rendered_html output_subarea {{ extra_class }}">\n{{ output.data[\'text/html\'] }}\n</div>\n{%- endblock data_html %}\n\n{% block data_markdown scoped -%}\n<div class="output_markdown rendered_html output_subarea {{ extra_class }}">\n{{ output.data[\'text/markdown\'] | markdown2html }}\n</div>\n{%- endblock data_markdown %}\n\n{% block data_png scoped %}\n<div class="output_png output_subarea {{ extra_class }}">\n{%- if \'image/png\' in output.metadata.get(\'filenames\', {}) %}\n<img src="{{ output.metadata.filenames[\'image/png\'] | posix_path }}"\n{%- else %}\n<img src="data:image/png;base64,{{ output.data[\'image/png\'] }}"\n{%- endif %}\n{%- set width=output | get_metadata(\'width\', \'image/png\') -%}\n{%- if width is not none %}\nwidth={{ width }}\n{%- endif %}\n{%- set height=output | get_metadata(\'height\', \'image/png\') -%}\n{%- if height is not none %}\nheight={{ height }}\n{%- endif %}\n{%- if output | get_metadata(\'unconfined\', \'image/png\') %}\nclass="unconfined"\n{%- endif %}\n{%- set alttext=(output | get_metadata(\'alt\', \'image/png\')) or (cell | get_metadata(\'alt\')) -%}\n{%- if alttext is not none %}\nalt="{{ alttext }}"\n{%- endif %}\n>\n</div>\n{%- endblock data_png %}\n\n{% block data_jpg scoped %}\n<div class="output_jpeg output_subarea {{ extra_class }}">\n{%- if \'image/jpeg\' in output.metadata.get(\'filenames\', {}) %}\n<img src="{{ output.metadata.filenames[\'image/jpeg\'] | posix_path }}"\n{%- else %}\n<img src="data:image/jpeg;base64,{{ output.data[\'image/jpeg\'] }}"\n{%- endif %}\n{%- set width=output | get_metadata(\'width\', \'image/jpeg\') -%}\n{%- if width is not none %}\nwidth={{ width }}\n{%- endif %}\n{%- set height=output | get_metadata(\'height\', \'image/jpeg\') -%}\n{%- if height is not none %}\nheight={{ height }}\n{%- endif %}\n{%- if output | get_metadata(\'unconfined\', \'image/jpeg\') %}\nclass="unconfined"\n{%- endif %}\n{%- set alttext=(output | get_metadata(\'alt\', \'image/jpeg\')) or (cell | get_metadata(\'alt\')) -%}\n{%- if alttext is not none %}\nalt="{{ alttext }}"\n{%- endif %}\n>\n</div>\n{%- endblock data_jpg %}\n\n{% block data_latex scoped %}\n<div class="output_latex output_subarea {{ extra_class }}">\n{{ output.data[\'text/latex\'] }}\n</div>\n{%- endblock data_latex %}\n\n{% block error -%}\n<div class="output_subarea output_text output_error">\n<pre>\n{{- super() -}}\n</pre>\n</div>\n{%- endblock error %}\n\n{%- block traceback_line %}\n{{ line | ansi2html }}\n{%- endblock traceback_line %}\n\n{%- block data_text scoped %}\n<div class="output_text output_subarea {{ extra_class }}">\n<pre>\n{{- output.data[\'text/plain\'] | ansi2html -}}\n</pre>\n</div>\n{%- endblock -%}\n\n{%- block data_javascript scoped %}\n{% set div_id = uuid4() %}\n<div id="{{ div_id }}"></div>\n<div class="output_subarea output_javascript {{ extra_class }}">\n<script type="text/javascript">\nvar element = $(\'#{{ div_id }}\');\n{{ output.data[\'application/javascript\'] }}\n</script>\n</div>\n{%- endblock -%}\n\n{%- block data_widget_state scoped %}\n{% set div_id = uuid4() %}\n{% set datatype_list = output.data | filter_data_type %} \n{% set datatype = datatype_list[0]%} \n<div id="{{ div_id }}"></div>\n<div class="output_subarea output_widget_state {{ extra_class }}">\n<script type="text/javascript">\nvar element = $(\'#{{ div_id }}\');\n</script>\n<script type="{{ datatype }}">\n{{ output.data[datatype] | json_dumps }}\n</script>\n</div>\n{%- endblock data_widget_state -%}\n\n{%- block data_widget_view scoped %}\n{% set div_id = uuid4() %}\n{% set datatype_list = output.data | filter_data_type %} \n{% set datatype = datatype_list[0]%} \n<div id="{{ div_id }}"></div>\n<div class="output_subarea output_widget_view {{ extra_class }}">\n<script type="text/javascript">\nvar element = $(\'#{{ div_id }}\');\n</script>\n<script type="{{ datatype }}">\n{{ output.data[datatype] | json_dumps }}\n</script>\n</div>\n{%- endblock data_widget_view -%}\n\n{%- block footer %}\n{% set mimetype = \'application/vnd.jupyter.widget-state+json\'%} \n{% if mimetype in nb.metadata.get("widgets",{})%}\n<script type="{{ mimetype }}">\n{{ nb.metadata.widgets[mimetype] | json_dumps }}\n</script>\n{% endif %}\n{{ super() }}\n{%- endblock footer-%}\n',
 'full.tpl': '{%- extends \'basic.tpl\' -%}\n{% from \'mathjax.tpl\' import mathjax %}\n\n\n{%- block header -%}\n<!DOCTYPE html>\n<html>\n<head>\n{%- block html_head -%}\n<meta charset="utf-8" />\n{% set nb_title = nb.metadata.get(\'title\', \'\') or resources[\'metadata\'][\'name\'] %}\n<title>{{nb_title}}</title>\n\n<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>\n\n{% block ipywidgets %}\n{%- if "widgets" in nb.metadata -%}\n<script>\n(function() {\n  function addWidgetsRenderer() {\n    var mimeElement = document.querySelector(\'script[type="application/vnd.jupyter.widget-view+json"]\');\n    var scriptElement = document.createElement(\'script\');\n    var widgetRendererSrc = \'{{ resources.ipywidgets_base_url }}@jupyter-widgets/html-manager@*/dist/embed-amd.js\';\n    var widgetState;\n\n    // Fallback for older version:\n    try {\n      widgetState = mimeElement && JSON.parse(mimeElement.innerHTML);\n\n      if (widgetState && (widgetState.version_major < 2 || !widgetState.version_major)) {\n        widgetRendererSrc = \'{{ resources.ipywidgets_base_url }}jupyter-js-widgets@*/dist/embed.js\';\n      }\n    } catch(e) {}\n\n    scriptElement.src = widgetRendererSrc;\n    document.body.appendChild(scriptElement);\n  }\n\n  document.addEventListener(\'DOMContentLoaded\', addWidgetsRenderer);\n}());\n</script>\n{%- endif -%}\n{% endblock ipywidgets %}\n\n{% for css in resources.inlining.css -%}\n    <style type="text/css">\n    {{ css }}\n    </style>\n{% endfor %}\n\n<style type="text/css">\n/* Overrides of notebook CSS for static HTML export */\nbody {\n  overflow: visible;\n  padding: 8px;\n}\n\ndiv#notebook {\n  overflow: visible;\n  border-top: none;\n}\n\n{%- if resources.global_content_filter.no_prompt-%}\ndiv#notebook-container{\n  padding: 6ex 12ex 8ex 12ex;\n}\n{%- endif -%}\n\n@media print {\n  div.cell {\n    display: block;\n    page-break-inside: avoid;\n  } \n  div.output_wrapper { \n    display: block;\n    page-break-inside: avoid; \n  }\n  div.output { \n    display: block;\n    page-break-inside: avoid; \n  }\n}\n</style>\n\n<!-- Custom stylesheet, it must be in the same directory as the html file -->\n<link rel="stylesheet" href="custom.css">\n\n<!-- Loading mathjax macro -->\n{{ mathjax() }}\n{%- endblock html_head -%}\n</head>\n{%- endblock header -%}\n\n{% block body %}\n<body>\n  <div tabindex="-1" id="notebook" class="border-box-sizing">\n    <div class="container" id="notebook-container">\n{{ super() }}\n    </div>\n  </div>\n</body>\n{%- endblock body %}\n\n{% block footer %}\n{{ super() }}\n</html>\n{% endblock footer %}\n',
 'mathjax.tpl': '{%- macro mathjax(url=\'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-AMS_HTML\') -%}\n    <!-- Load mathjax -->\n    <script src="{{url}}"></script>\n    <!-- MathJax configuration -->\n    <script type="text/x-mathjax-config">\n    MathJax.Hub.Config({\n        tex2jax: {\n            inlineMath: [ [\'$\',\'$\'], ["\\\\(","\\\\)"] ],\n            displayMath: [ [\'$$\',\'$$\'], ["\\\\[","\\\\]"] ],\n            processEscapes: true,\n            processEnvironments: true\n        },\n        // Center justify equations in code and markdown cells. Elsewhere\n        // we use CSS to left justify single line equations in code cells.\n        displayAlign: \'center\',\n        "HTML-CSS": {\n            styles: {\'.MathJax_Display\': {"margin": 0}},\n            linebreaks: { automatic: true }\n        }\n    });\n    </script>\n    <!-- End of mathjax configuration -->\n{%- endmacro %}\n',
 'celltags.tpl': "{%- macro celltags(cell) -%}\n    {% if cell.metadata.tags | length > 0 -%}\n        {% for tag in cell.metadata.tags -%}\n            {{ ' celltag_' ~ tag -}}\n        {%- endfor -%}\n    {%- endif %}\n{%- endmacro %}\n"
}