#ifndef __FACE_DETECTION_HPP__
#define __FACE_DETECTION_HPP__

// for OpenCV2
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/gpu/gpu.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/video/video.hpp>

#include <iostream>

class FaceDetection
{
private:
    std::string fullbodyCascadeFilename;
    cv::CascadeClassifier fullbodyDetector;
    cv::VideoCapture capture;

public:
    FaceDetection(int cameraIndex)
    {
        fullbodyCascadeFilename = "./lbpcascades/hogcascade_pedestrians.xml";

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

        capture.open("outputfile.mpeg");
        if (!capture.isOpened()) // check if we succeeded
        {
            printf("No camera was found.\n");
            exit(1);
        }
    }

    ~FaceDetection()
    {
        // capture.release();
    }

    void doDetection()
    {
        capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);
        capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);

        cv::BackgroundSubtractorMOG2 bgr (100, 16, false);
        bgr.set("nmixtures", 3);

        cv::namedWindow("full_body", 1);
        // cv::namedWindow("Background Model");
        // cv::namedWindow("Blob");

        cv::Mat image;
        cv::Mat fg;
        cv::Mat blurred;
        cv::Mat thresholded;
        cv::Mat gray;
        cv::Mat blob;
        cv::Mat bgmodel;

        cv::Size minFeatureSize(80, 80);     // Smallest face size.
        std::vector<std::vector<cv::Point>> contours;
        for (;;)
        {

            capture >> image ; // get a new frame from camera

            if (image.empty())
                std::cout << "boomp" << std::endl;

            cv::GaussianBlur(image, blurred, cv::Size(3, 3), 0, 0, cv::BORDER_DEFAULT);

            bgr.operator()(blurred, fg);


            // bgr.getBackgroundImage(bgmodel);

            // cv::threshold(fg, thresholded, 70.0f, 255, CV_THRESH_BINARY);
            cv::adaptiveThreshold(fg, thresholded, 255, CV_ADAPTIVE_THRESH_MEAN_C, CV_THRESH_BINARY, 9, 1);
            // cv::imshow("Blob", thresholded);

            // cv::Mat elementCLOSE(5, 5, CV_8U, cv::Scalar(255, 255, 255));
            // cv::morphologyEx(thresholded, thresholded, cv::MORPH_CLOSE, elementCLOSE);

            // cv::findContours(thresholded, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
            // cv::cvtColor(thresholded, blob, CV_GRAY2RGB);
            // cv::drawContours(blob, contours, -1, cv::Scalar(1), CV_FILLED, 8);

            cv::cvtColor(image, gray, CV_RGB2GRAY);
            cv::equalizeHist(gray, gray);

            // int cmin = 500;
            // int cmax = 1000;
            std::vector<cv::Rect> rects;

            fullbodyDetector.detectMultiScale(gray, rects, 1.1, 3, 0, minFeatureSize);

            for (std::size_t i(0); i < rects.size(); i++)
            {
                // cv::Mat imageROI = image(bodys[i]);

                cv::rectangle(image, rects[i], cv::Scalar( 255, 0, 0 ), 1, 8, 0);
            }


            // std::vector<std::vector<cv::Point>>::iterator itc = contours.begin();

            // while (itc != contours.end())
            // {
            //
            // if (itc->size() > cmin && itc->size() < cmax)
            // {

            // fullbodyDetector.detectMultiScale(gray, rects);
            // for (unsigned int i = 0; i < rects.size(); i++)
            // {
            // cv::rectangle(image, cv::Point(rects[i].x, rects[i].y),
            // cv::Point(rects[i].x + rects[i].width, rects[i].y + rects[i].height),
            // cv::Scalar(0, 255, 0));
            // }
            //
            // ++itc;
            // }
            // else
            // {
            // ++itc;
            // }
            // }

            cv::imshow("full_body", image);
            // cv::imshow("Background Model", bgmodel);

            if (cv::waitKey(30) == 27)
                break;
            // }
        }
    }
};

#endif /* __FACE_DETECTION_HPP__ */