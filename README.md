# pdf-scraper-with-ocr
With this tool I am aiming to facilitate the work of those who need to scrape PDFs either by hand or using tools that doesn't implement any kind of character recognition.

[![Screencast](https://github.com/JacoboGuijar/pdf-scraper-with-ocr/blob/main/demos/Usage%20demo.gif)](https://github.com/JacoboGuijar/pdf-scraper-with-ocr/blob/main/demos/Usage%20demo.gif)


## How it works
When you run the program a GUI will open with four buttons. Only two of them are available for use at the begining: "Choose a PDF" and "Extract Information". We will start choosing our PDF. When the button is clicked a new window will open where we can navigate through our folders and select the PDF we want.

Once we have selected the PDF the button "Delete Pages" will activate. Here we will be able to select which pages we want to delete from our PDF because they do not contain information we want to scrape. Do not worry, the program will create a copy of your PDF and modify the copy, it will not touch the original except to create the copy. In case you do not want to delete any pages just leave the field in blank, however, if our PDF contains a cover, index or other kind of one time only pages you can delete them by indicating each page separated by a semicolon, see: `1;2;10;` this will delete pages 1, 2 and 10. If you want to delete a range of pages you can indicate the first and last page separated by a hyphen: `5-10` will delete pages 5, 6, 7, 8, 9 and 10. See below for other commands.

Now that we have deleted the pages we did not need the button "PDF to images" will activate, pressing it will open a window where we will be asked to select the folder where the pages of the PDF will be saved as images. If the PDF has over 100 pages this might take a while (around 25 minutes for 456 pages in my case). It might look like the window freezes but do not worry, the program is still running.

Finally, once all the pages have been converted to images we can start scraping the PDF. By clicking on "Extract Information" the window will change and present four new buttons: "Load images", "Undo", "Show image" and "Extract text". Clicking on "Load images" will open a window where we can select the folder where our images where saved. Once we have selected the folder we will be asked if our PDF follows any pattern. A pattern is used whenever the information we want to obtain is divided in different pages. Maybe the phone number of a client is in one page and the email in the next one, however we must be sure that every client will follow this pattern and have the phone number and email in the same place. In case our information is not split across diferent pages we can write 1, as the pattern will repeat every page. We will also need to choose if we want to see random images or not. We will select not randomized by now, see below for information. 

Whenever we click on "ok" the program will load a series of preview images where we can select by clicking and draggin the information we want to keep. Every time we start clicking a red rectangle will follow the mouse until the click is released. After releasing the mouse we will be asked what is the name of the field we just selected. This name will be the name of the column where this is information is stored. After creating as many selections as we want we can click on "Extract text". Go grab a coffe, this might take a long time but after finishing a new file will appear in the folder where you are running this script. An Excel file with all the information you wanted.

You can find a series of demos and step by step tutorials in different formats in the 'demos' folder.

## Language configuration and field naming
There are multiple types of texts that can be extracted. Here I will explain the different solutions to improve your text extraction.

If your main language is not English please change the value of the 'MY_LANG' variable at the begging of the 'pdf-scraper-with-ocr.py' file to the language you need. You can find the different languages in the [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/Data-Files.html). 

It should be noticed that if you want to extract an email the '@' symbol will not be detected some times. To improve the accuracy of the email detection you can add '\_email' at the end of the name selection. See:

![](https://i.imgur.com/gughskB.png)

This will change the language to English only for this selection, something that seems to help a lot in the email detection.

This program is configured to analyze only one line, as you can see in the demos files. In case you need to analyze a field of text that is divided in multiple lines you should add at the end of the selection '\_ML'. This will tell the program that this specific field has multiple lines. 

Different features for different types of text will be added in the future

## Deleting pages
Every PDF is different from others. They can be organized in a lot of different ways, making the automation of the pages to delete kind of a pain. Currently this are the commands supported for deleting pages:
### Single page deletion
This will delete the pages that to correspond to the written indexes: `1;2;10;` will delete pages 1, 2 and 10.
### Delete page in range
This will delete the pages between the first and last index seperated by a hyphen: `5-10` will delete pages 5, 6, 7, 8, 9 and 10.
### Delete every Nx pages:
If every three files in our PDF we have a file that does not have any interesting information by using. `Nx` we will delete every index multiple of N. `3x` will delete pages 3, 6, 9, 12, 15...
### Delete every Nx + C pages:
Maybe the pattern our PDF follows goes like this: page 1 (useful), page 2 (useless), page 3 (useful),(the pattern begins again here) page 4 (useful)... We will need to delete pages 2, 5, 8, 11... Then using `3x+1` will delete every three pages the next page.
### Delete everything after or before N:
In case we want to delete all pages after page N using: `N-` will delete every page after page N. In the same way, using: `-N` will delete all pages before N. 
### Combinations
You can combine different methods to delete pages separating them by a semicolon: `4x; 100-; 45;` this will delete every fourth page, all pages after index 100 and the page 45.

## The Show image button
It is important that you make sure all your selections grab all the information in all pages. To help you create better selections you can click on the "Show image" button to navigate across different pages. If you have a pattern of 1 you will see that every time you click on the button your image change but the rectangles stay in place. In case you want to delete any of them you can use the "Undo" button (explanation below). If you have a pattern greater than 1 when clicking on "Show image" you will see how your selections disappear. This is because the program keeps track of what selections you have made in which page of the pattern. You can also create selections here that will be analyzed next to the ones in the previous page.

## Randomized preview
Selecting to randomize the preview images can be quite helpful. Many times every section in a PDF seems to follow the same pattern and fill the same space but every now and them some fields might not be were they should or some piece of text might be bigger than rectangle you created before. This is were the randomized preview can save your output file. Keep in mind that the random preview will keep showing images in order according to the pattern you selected, you will just see different patterns instead of the three first ones that the not randomized option offers.

## The Undo button
In case you clicked something by mistake, did not write correctly the name you wanted for a field or created a rectangle that later you discovered will not capture all the info you wanted there is an undo button. The Undo button will eliminate the last rectangle created. In case your PDF follows a pattern greater than 1 the undo button will delete the last rectangle created in the page you are. For example, if your PDF has a pattern of 3 and you have created two rectangles on page 1, then click on "Show image" to see the next image in your pattern (page 2) and create a rectangle there and go back to page 1 (by clicking twice on "Show image"), clicking the undo button will not delete the selection from page 2, it will delete the last created selection in the page you are at the moment of clicking.
