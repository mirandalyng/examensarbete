{% macro is_latin_text(column) %}
    -- Tillåter: latinska bokstäver inkl. diakritiska (À-ÖØ-öø-ÿ, Latin Extended-A/B: Ā-ɏ),
    -- siffror, mellanslag, apostrofer (' ’ ‘) och vanlig skiljetecken.
    regexp_matches(
        {{ column }},
        '^[A-Za-z0-9\x{00C0}-\x{00D6}\x{00D8}-\x{00F6}\x{00F8}-\x{024F}\x{1E00}-\x{1EFF} \x27\x{2018}\x{2019}\.,!?&:;()\[\]/+*#@%$"\-\x{2013}\x{2014}_~|=<>]*$'
    )
{% endmacro %}