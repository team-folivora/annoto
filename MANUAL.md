# Annoto Manual for users

Opening the web app will confront you with a login dialog. The test user is `Annoto#1337` with password `test1234`. Press the button to login.

You will then see a dialogue window, asking you to confirm that you have 1) read this Manual and 2) are attentive and in the proper condition to annotate images.

After confirming, you will see an image. Below the image there are buttons with labels that can be used to annotate the image. Without confirming, it is not possible to proceed annotating the images.

Click on one of the annotation buttons to create an annotation for the displayed image. The annotation is then stored into the `.annoto`-folder in the home directory of your local file system. The application will now present you a new image.

As long as you are not in a production environment, you can view & remove the contents of this `.annoto` folder using the API-route `/debug/data`.
