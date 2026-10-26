{% macro parse_list(col) -%}
list_filter(
    list_transform(
        string_split(regexp_replace({{ col }}, '^\[|\]$', '', 'g'), ', '),
        x -> trim(x, chr(39) || chr(34))
    ),
    x -> x <> ''
)
{%- endmacro %}