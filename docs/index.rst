장고 ORM 요리책
+++++++++++++++++++++++


『장고 ORM 요리책(Django ORM Cookbook)』은 장고의 ORM과 모델을 이용한 다양한 레시피(조리법)를 담은 책입니다. 장고는 모델-템플릿-뷰(MTV) 프레임워크입니다. 이 책에서는 그 가운데 '모델'에 대해 상세히 다룹니다.

이 책은 "장고 ORM/쿼리셋/모델으로 ~을 하는 방법은 무엇인가요?"와 같은 질문 50여 개와 그 답을 담고 있습니다.


.. image:: BookCover.jpg

.. toctree::
   :maxdepth: 1

   introduction


정보를 질의하고 걸러내기
========================

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


정보를 생성/갱신/삭제하기
=======================

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


질의 결과를 정렬하기
========================

.. toctree::
   :maxdepth: 1
   :numbered:

   asc_or_desc
   case_insensitive
   order_by_two
   order_by_related_model
   order_by_annotated_field


데이터베이스 모델 짜기
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




테스트하기
===============================================
.. toctree::
   :maxdepth: 1
   :numbered:

   numqueries
   keepdb
   refresh_from_db



찾아보기 / 표
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

