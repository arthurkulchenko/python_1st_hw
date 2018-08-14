<html>
	<head>
		<style type="text/css">
		 .img{
		 	margin: -70px -50px -123px 500px;
		 	background: red;
		 }
		</style>
	</head>
	<body>
		<img src="https://otus.ru/static/img/favicons/android-chrome-537x240.jpg" class="img">
	</body>
</html>
## Second homework
### Lesson tasks
Нужно доработать скрипт из первого задания. Вот что он должен уметь:

 ✔︎ принимать все аргументы через консольный интерфейс. (v0.2.1)
 
 ✘ клонировать репозитории с Гитхаба;
 
 ✘ выдавать статистику самых частых слов по глаголам или существительным (в зависимости от параметра отчёта);
 
 ✘ выдавать статистику самых частых слов названия функций или локальных переменных внутри функций (в зависимости от параметра отчёта);
 
 ✘ выводить результат в консоль, json-файл или csv-файл (в зависимости от параметра отчёта);

### Keep in mind

- получение кода из других места, не только с Гитхаба;
- парсеры других ЯП, не только Python;
- сохранение в кучу разных форматов;
- более сложные типы отчётов (не только частота частей речи в различных местах кода).

[source](https://gist.github.com/Melevir/5754a1b553eb11839238e43734d0eb79)

### How to use
To make use simply run `python scan_file.py` + `key` and `value`
for very beginnig you can try `-h` or just skip any of keys.