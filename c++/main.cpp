#include <iostream>

// for OpenCV2
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/gpu/gpu.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/video/tracking.hpp"

#include "FaceDetection.hpp"

int main(int argc, char **argv)
{
    FaceDetection faceObj(0);
    faceObj.doDetection();
/*
    std::string fullbodyCascadeFilename = "./lbpcascades/lbpcascade_frontalface.xml";
    // std::string fullbodyCascadeFilename = "./haarcascades/haarcascade_fullbody.xml";
    cv::CascadeClassifier fullbodyDetector;

    try
    {
        fullbodyDetector.load(fullbodyCascadeFilename);
    }
    catch (cv::Exception e) {}
    if ( fullbodyDetector.empty() )
    {
        std::cerr << "ERROR: Couldn't load Full Body Detector (";
        std::cerr << fullbodyCascadeFilename << ")!" << std::endl;
        exit(1);
    }

    cv::VideoCapture capture(0); // open the default camera
    if (!capture.isOpened()) // check if we succeeded
    {
        printf("No camera was found.\n");
        return -1;
    }
    capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);
    capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);

    cv::namedWindow("full_body", 1);

    cv::Mat image, grayImage;
    cv::Size minFeatureSize(80, 80);     // Smallest face size.
    std::vector < cv::Rect > bodys;
    for(;;)
    {
        capture >> image ; // get a new frame from camera

        cv::cvtColor(image, grayImage, CV_BGR2GRAY);

        // Standardize the brightness & contrast, such as // to improve dark images.
        cv::equalizeHist(grayImage, grayImage);

        fullbodyDetector.detectMultiScale(grayImage, bodys, 1.1, 3, 0, minFeatureSize);

        for(std::size_t i(0); i<bodys.size(); i++)
        {
            cv::rectangle(image,bodys[i],cv::Scalar( 0, 255, 0 ), 3, 8, 0);
        }

        cv::imshow("full_body", image);

        if (cv::waitKey(30) == 27)
            break;
    }
    */
    return 0;
}