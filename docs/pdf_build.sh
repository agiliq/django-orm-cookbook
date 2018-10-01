sphinx-build -b latex . _build/latex
sed -i '' 's/\[T1\]{fontenc}/{kotex}/g' ./_build/latex/DjangoORMCookbook.tex
sed -i '' 's/{babel}/\[english\]{babel}/g' ./_build/latex/DjangoORMCookbook.tex
sed -i '' '/BookCover/d' ./_build/latex/DjangoORMCookbook.tex

cd ./_build/latex/ && make all-pdf && cd -
