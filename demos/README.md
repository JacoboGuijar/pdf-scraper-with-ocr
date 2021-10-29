# The demos folder
Here you will find examples on gif and image formats, as well as the PDFs I used for creating the tutorials and doing some testing. 

This file is also an step by step guide to analyze the three demos you can find in this folder to help you get used to this application.

## Analyzing 'demo_no_jumps.pdf'
This file is the most simple case for analyzing as it will not require eliminating any images and it have a pattern of 1 as every page has a different content but with the same layout.

Click on 'Choose a PDF' to select the file, then on 'Delete Pages'. As said before, we want to keep all the pages in this PDF so we will leave the field where we were supossed to introduce the pages indexes in blank and just click on 'ok'. Clicking in 'PDF to images' will ask to introduce a name for a folder were we will save the pages as images, for this tutorial it will be named as the file, 'demo_no_jumps' (which you can also find in this folder). If done correctly 'demo_no_jumps' should contain three images that correspond to three pages of the PDF. 

Now that we have the images we can click on 'Extract Information' to start the selection process. First select the folder where the images were saved by clicking on 'Load images'. Once the folder have been selected a new window will appear. Here we need to introduce the pattern that the PDF follows and if we want to see a randomized selection of the pages or see them in order. Because our PDF has every page the same layout and each page correspond to the information of a different client we know that the pattern is 1. The randomized option must be filled but whatever we choose it will not affect the PDF or the order in which the information is extracted, just the images we see.

After clicking on 'ok' you are ready to start selecting everything you need and whenever you finish you can click on 'Extract text' to export each field into an xlsx file.

## Analyzing 'demo_jumps_not_interesting_pages.pdf'
Start taking a look to the PDF. In this case some pages have useless information. We can fix this by using the deleting function. It is ease to spot that the pages we want to delete appear every two files. 

Open the PDF and click on 'Delete Pages'. If you have read the README on the main page of this project you might have seen the Deleting pages section. There you can find one of the commands that works perfectly for this kind of files: `Nx`. This will delete one page every N pages. In our case writting `2x` in the deleting field will delete all the pages we do not want. After clicking on 'ok' you can click on 'PDF to images' to see the resulting images or simply go to the folder where you are running the program to see the 'temp.pdf' created after the deleting process. Remember you can find in this folder the container for the images too.

Finally go to 'Extract Information' and 'Load images' to select the images folder and select the pattern. In this case once all the unwanted pages have been deleted the PDF will have a pattern of 1, as in the previous example. Select if you want to randomize the preview images or not and start selecting the sections you need.

## Analyzing 'demo_jumps_interesting_pages_pattern_2.pdf'
Opening this file will display a PDF where the information we want to obtain is divided in two pages. The main page that we have seen in the previous examples and an extra one contains extra info about the clients. All of the pages contain important information so we will not delete any of them but rather change how the images are displayed and saved to obtain everything we need.

Start by opening the PDF and clicking on 'Delete Pages'. Leave the field in blank, click on 'PDF to images' and then on 'Extract Information'. Once the folder has been selected we will be asked what pattern follows our PDF. As the information we want is divided in two pages we want to save every two pages as one client in the output file. To accomplish that write that the PDF has a pattern of 2. Select if you want the output randomized or not and click on 'ok'.

Once the images are loaded you can navigate through them by clicking on 'Show image'. We will see first the main page we have seen in other examples and then the new extra page. Now you have two different pages to select the information you want to extract. I encourage you to play around creating selections across the different fields. 

One thing to notice is that if you use the 'Undo' button it will not delete the last rectangle you made. It will delete the last rectangle you made on the page you are when you click the button. Let's see a couple of examples: First, you create two selections on the main page and then change to the extra page where you have not done any selections yet and click the 'Undo' button. It will not delete anything as there are no selections on the extra page. Second, if you create two selections on page one, change to page two and create other selections and change again to page one. Now you decide that one of your selections doesn't contain all the info in every page so you decide to click the Undo button. It will change the last selection on page one because even though the last selection is on page two the 'Undo' button will delete the last selection in the page you are when clicking it.

# Analyzing 'demo_final_example.pdf'
In this file we will use the deleting images utility and the pattern selection. Taking a look to the file it might take a couple of minutes to discover that this file has a page we want to delete every page after a multiple of three. The deleting command used for this has the form `Nx+C` and for this particular case is `3x+1`. 

If you now open the temp.pdf or see the folder where the images are saved you can see that we now have a file like the one analyzed on the previous example. Following the same logic introduce a pattern of 2 and begin selecting the areas you need.
