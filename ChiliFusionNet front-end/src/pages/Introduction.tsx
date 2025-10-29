import React from 'react';

export const Introduction: React.FC = () => {
  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          Introduction
        </h1>
        
        {/* Page Navigation */}
        <div className="flex flex-wrap gap-4 mb-8">
          <a 
            href="#abstract" 
            className="inline-flex items-center px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-800 transition-colors text-sm font-medium"
          >
            Abstract
          </a>
          <a 
            href="#background" 
            className="inline-flex items-center px-4 py-2 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-lg hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors text-sm font-medium"
          >
            Background & Motivation
          </a>
        </div>
        
        {/* Abstract Section */}
        <div id="abstract" className="bg-neutral-50 dark:bg-neutral-800 p-8 rounded-xl border border-neutral-200 dark:border-neutral-700 mb-12">
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-6">
            Abstract
          </h2>
          <div className="prose dark:prose-invert max-w-none">
            <p className="text-lg text-neutral-700 dark:text-neutral-300 leading-relaxed mb-4">
              Chili pepper crops are susceptible to various diseases that significantly impact agricultural productivity and economic returns. Traditional manual inspection methods for disease detection are time-consuming, subjective, and often lead to delayed treatment. This paper presents ChiliFusionNet, a novel ensemble deep learning framework designed for accurate and efficient classification of chili leaf diseases.
            </p>
            <p className="text-lg text-neutral-700 dark:text-neutral-300 leading-relaxed mb-4">
              Our proposed methodology combines multiple state-of-the-art convolutional neural network architectures through an advanced ensemble learning approach, achieving superior performance in distinguishing between healthy leaves and various disease conditions including Bacterial Spot, Cercospora Leaf Spot, Curl Virus, Nutrition Deficiency, and White Spot.
            </p>
            <p className="text-lg text-neutral-700 dark:text-neutral-300 leading-relaxed">
              Experimental results demonstrate that ChiliFusionNet achieves an accuracy of [XX]% on our comprehensive dataset, outperforming individual CNN models and existing approaches. This research contributes to the advancement of precision agriculture by providing farmers with an automated, reliable tool for early disease detection and management.
            </p>
          </div>
          
          <div className="mt-6 pt-6 border-t border-neutral-200 dark:border-neutral-700">
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
                Deep Learning
              </span>
              <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
                Ensemble Learning
              </span>
              <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
                Plant Disease Detection
              </span>
              <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
                Computer Vision
              </span>
              <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
                Precision Agriculture
              </span>
            </div>
          </div>
        </div>

        {/* Introduction Content */}
        <div id="background" className="prose dark:prose-invert max-w-none">
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-6">
            Background and Motivation
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
            Early detection of plant diseases is crucial for maintaining agricultural productivity 
            and ensuring food security. In the context of smart agriculture, deep learning and 
            machine learning pipelines have revolutionized the way we approach plant disease detection.
          </p>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
            ChiliFusionNet represents a significant advancement in chili leaf disease detection, 
            leveraging ensemble learning techniques to achieve superior accuracy and reliability 
            compared to traditional single-model approaches.
          </p>
          
          <h3 className="text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
            Problem Statement
          </h3>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            Chili peppers are among the most economically important crops globally, but they are highly 
            susceptible to various diseases that can cause significant yield losses. Current manual 
            inspection methods are:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-neutral-600 dark:text-neutral-400 mb-6">
            <li>Time-consuming and labor-intensive</li>
            <li>Subjective and prone to human error</li>
            <li>Difficult to scale for large agricultural operations</li>
            <li>Often result in delayed diagnosis and treatment</li>
          </ul>

          <h3 className="text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
            Research Objectives
          </h3>
          <p className="text-neutral-600 dark:text-neutral-400 mb-4">
            This research aims to develop an automated system that can:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-neutral-600 dark:text-neutral-400">
            <li>Accurately classify multiple chili leaf diseases from digital images</li>
            <li>Provide real-time diagnosis capabilities for field deployment</li>
            <li>Outperform existing single-model approaches through ensemble learning</li>
            <li>Support early intervention strategies for disease management</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
