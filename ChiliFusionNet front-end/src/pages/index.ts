export { Abstract } from './Abstract';

export const Method: React.FC = () => (
  <div className="section-padding">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-8">Methodology</h1>
      <p>TODO: IEX-FeatureNet feature extraction and ChiliFusionNet ensemble details</p>
    </div>
  </div>
);

export const Results: React.FC = () => (
  <div className="section-padding">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-8">Results</h1>
      <p>TODO: Accuracy, F1 scores, confusion matrix, ROC curves from Results PDF</p>
    </div>
  </div>
);

export const Dataset: React.FC = () => (
  <div className="section-padding">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-8">Dataset</h1>
      <p>TODO: 6 classes dataset information</p>
    </div>
  </div>
);

export const Demo: React.FC = () => (
  <div className="section-padding">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-8">Demo</h1>
      <p>TODO: Side-by-side inference UI with drag-and-drop</p>
    </div>
  </div>
);

export const Team: React.FC = () => (
  <div className="section-padding">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-8">Team</h1>
      <p>TODO: Research team information</p>
    </div>
  </div>
);

export const References: React.FC = () => (
  <div className="section-padding">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-8">References</h1>
      <p>TODO: Citations to research papers</p>
    </div>
  </div>
);

export const NotFound: React.FC = () => (
  <div className="section-padding text-center">
    <div className="container-width">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
    </div>
  </div>
);
