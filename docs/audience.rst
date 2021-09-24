===============
Target audience
===============

Who is the target audience of the bibrecord package? Is it interesting for me?

The bibrecord package aims at scientists and developers of data processing and analysis software. Often when implementing such software, we would like to give credit to the original authors of algorithms we implement, or otherwise to refer to the literature.

As in science, BibTeX has been used since decades, particularly in conjunction with TeX/LaTeX as typesetting system, it feels quite natural to provide a structure similar to a BibTeX record fits neatly within the code. Therefore, of you develop algorithms and use the paradigma of object-oriented programming (OOP), adding a (list of) bibliographic record(s) as property to your class would be a simple thing.

Thanks to the capabilities of the bibrecord classes to return a string representation of a record (as well as a BibTeX record), you can easily reuse the information stored within your code.
