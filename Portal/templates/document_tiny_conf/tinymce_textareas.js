tinyMCE.init({
    mode: "textareas",
    theme: "dark",
    {% comment %} plugins: "spellchecker,directionality,paste,searchreplace",
    language: "{{ language }}",
    directionality: "{{ directionality }}",
    spellchecker_languages : "{{ spellchecker_languages }}",
    spellchecker_rpc_url : "{{ spellchecker_rpc_url }}" {% endcomment %}
});