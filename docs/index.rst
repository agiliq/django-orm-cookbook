장고 ORM 요리책
+++++++++++++++++++++++


장고 ORM 요리책은 장고 ORM 과 장고의 모델을 사용하는 방법에 관한 책입니다.
장고는 "MTV"(모델-템플릿-뷰) 프레임워크입니다 - 이 책은 모델 파트에 대한 내용을 자세히 다룹니다.

이 책은 장고 ORM/쿼리셋/모델의 사용법에 관한 50가지의 질문으로 구성되어 있습니다.

.. image:: BookCover.jpg

.. toctree::
   :maxdepth: 1

   introduction

Querying and Filtering
===============================================

.. toctree::
   :maxdepth: 1
   :numbered:

   query
   or_query
   and_query
   notequal_query
   union
   select_some_fields
   subquery
   f_query
   filefield
   join
   second_largest
   duplicate
   distinct
   query_relatedtool
   aggregation
   random
   func_expressions


Creating, Updating and Deleting things
===============================================

.. toctree::
   :maxdepth: 1
   :numbered:

   multiple_objects
   copy
   singleton
   update_denormalized_fields
   truncate
   signals
   datetime


Ordering things
========================

.. toctree::
   :maxdepth: 1
   :numbered:

   asc_or_desc
   case_insensitive
   order_by_two
   order_by_related_model
   order_by_annotated_field


Database Modelling
==============================================

.. toctree::
   :maxdepth: 1
   :numbered:

   one_to_one
   one_to_many
   many_to_many
   self_fk
   existing_database
   database_view
   generic_models
   table_name
   column_name
   null_vs_blank
   uuid
   slugfield
   multiple_databases




Testing
===============================================
.. toctree::
   :maxdepth: 1
   :numbered:

   numqueries
   keepdb
   refresh_from_db

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
