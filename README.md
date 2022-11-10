# YOLO-Dataset-Toolkit

## Index
1.[Image Tools](#1.Image-Tools)   
    └ a.[Compare Label](#Compare-Label)   
    └ b.[Augmentation LetterBox](#Augmentation-LetterBox)   
    └ c.[Augmentation Mirror](#Augmentation-Mirror)   
    └ d.[Augmentation Motion Blur](#Augmentation-Motion-Blur)   
    └ e.[Censor](#Censor)   

2.[Other Tools](#2.Other-Tools)   
    └ a.[Count Class](#Count-Class)   
    └ b.[Check Duplication](#Check-Duplication)   
    
    
## 1.Image Tools
> This is original image.
![engin-akyurt-WBM97UGM0QA-unsplash](https://user-images.githubusercontent.com/97486738/199654238-b0f392aa-4ccb-407d-b75d-fff29c618d31.jpg)



### Compare Label
![sample](https://user-images.githubusercontent.com/97486738/199668616-eef13d3c-4928-46ef-99e2-f98f4f501e52.jpg)
You can compare model results with ground truth. Left one is the model result.


### Augmentation LetterBox
![engin-akyurt-WBM97UGM0QA-unsplash_letter](https://user-images.githubusercontent.com/97486738/199421470-261adba3-cc29-4604-9d7f-5caad7440c2e.jpg)
You can make a smaller image for bbox diversity like this. You can customize the letterbox color, and labels will convert automatically.


### Augmentation Mirror
![engin-akyurt-WBM97UGM0QA-unsplash_mirror](https://user-images.githubusercontent.com/97486738/199422839-112d6365-0cba-4d14-a918-a5b36a9f4463.jpg)
You can make an image that is flipped horizontally.


![result](https://user-images.githubusercontent.com/97486738/199423354-c6cf27fc-ddbe-4caf-9a01-4b2b9731fcfd.png)                                
This is an example of a result.



### Augmentation Motion Blur
![engin-akyurt-WBM97UGM0QA-unsplash_motion](https://user-images.githubusercontent.com/97486738/199654418-34206493-0c96-4c24-926f-5ae64179c722.jpg)
You can add motion blur to your data. Maybe it can increase the accuracy of real-time detection.



### Censor
![sample](https://user-images.githubusercontent.com/97486738/199657511-ede48c1f-fa13-43ac-ab3b-e000a7b16fb7.jpg)
You can censor useless data on the image.


## 2.Other Tools
### Count Class
![image](https://user-images.githubusercontent.com/97486738/201023143-a67b4ac2-7196-4308-958b-84e5c7cb586a.png)                                           
Count class like this. No matter there is how many classes.

### Check Duplication
![image](https://user-images.githubusercontent.com/97486738/201038744-938aa71b-e035-49b4-812d-6e732a4f1ba5.png)                                                   
Use to find filename duplication. It is useful to check test/validation set leakage. You can make log file.
