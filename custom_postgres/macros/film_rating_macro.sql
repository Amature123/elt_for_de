{% macro generate_film_rating_sql() %}
WITH films_writings AS (
  SELECT 
    film_id,
    title,
    release_date,
    price,
    rating,
    user_rating,
    {{rating_case()}} 
  FROM {{ref('films')}}
),
films_with_actors AS (
  SELECT
    f.film_id,
    f.title,
    STRING_AGG(a.actor_name, ',') AS actors
  FROM {{ref('films')}} AS f
  LEFT JOIN {{ref('film_actors')}} AS fa ON f.film_id = fa.film_id
  LEFT JOIN {{ref('actors')}} AS a ON fa.actor_id = a.actor_id 
  GROUP BY f.film_id, f.title
)
SELECT
  fw.*,
  fwa.actors
FROM films_writings fw
LEFT JOIN films_with_actors fwa ON fw.film_id = fwa.film_id
{% endmacro %}