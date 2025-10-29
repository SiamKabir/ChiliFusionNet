import React from 'react';

export const Method: React.FC = () => {
  return (
    <div className="section-padding">
      <div className="container-width">
        <h1 className="text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-8">
          Methodology
        </h1>
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-6">
            TODO: Extract methodology from introduction chili.pdf
          </p>
          <h2>IEX-FeatureNet Feature Extraction</h2>
          <p>TODO: Add details about feature extraction methodology</p>
          
          <h2>ChiliFusionNet Ensemble</h2>
          <p>
            Our ensemble approach combines multiple machine learning algorithms:
          </p>
          <ul>
            <li>XGBoost</li>
            <li>LightGBM (LGBM)</li>
            <li>Random Forest (RF)</li>
            <li>Extra Trees</li>
            <li>Logistic Regression (LR) meta-learner</li>
          </ul>
          
          <div className="mt-8 p-6 bg-neutral-100 dark:bg-neutral-800 rounded-xl">
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              TODO: Add methodology diagram placeholder
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
