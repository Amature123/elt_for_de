{% macro rating_case() %}
  CASE 
      WHEN user_rating >= 4.5 THEN 'EXCELLENT'
      WHEN user_rating >= 4.0 THEN 'VERY GOOD'
      WHEN user_rating >= 3.0 THEN 'GOOD'
      ELSE 'POOR'
    END AS user_rating_category
{% endmacro %}