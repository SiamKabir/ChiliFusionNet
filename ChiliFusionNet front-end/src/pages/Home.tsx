import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowRight, 
  Zap, 
  Shield, 
  Brain, 
  TrendingUp, 
  Mail,
  Linkedin,
  Github,
  ChevronUp
} from 'lucide-react';
import { Demo } from './Demo';

export const Home: React.FC = () => {
  const [showScrollTop, setShowScrollTop] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // Hero images data
  const heroImages = [
    {
      src: '/Hero images/healthy.png',
      label: 'Healthy Leaf',
      description: 'Detecting healthy chili leaves',
      color: 'from-green-400 to-emerald-500'
    },
    {
      src: '/Hero images/bacterial.png',
      label: 'Bacterial Spot',
      description: 'Identifying bacterial infections',
      color: 'from-red-400 to-rose-500'
    },
    {
      src: '/Hero images/cercospora.png',
      label: 'Cercospora Leaf Spot',
      description: 'Spotting cercospora diseases',
      color: 'from-orange-400 to-amber-500'
    },
    {
      src: '/Hero images/curl.png',
      label: 'Curl Virus',
      description: 'Detecting viral infections',
      color: 'from-purple-400 to-violet-500'
    },
    {
      src: '/Hero images/nutri.png',
      label: 'Nutrition Deficiency',
      description: 'Identifying nutrient deficiencies',
      color: 'from-yellow-400 to-orange-500'
    },
    {
      src: '/Hero images/white.png',
      label: 'White Spot',
      description: 'Detecting white spot diseases',
      color: 'from-blue-400 to-cyan-500'
    }
  ];

  // Auto-rotate hero images
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => 
        (prevIndex + 1) % heroImages.length
      );
    }, 4000); // Change image every 4 seconds

    return () => clearInterval(interval);
  }, [heroImages.length]);

  // Handle scroll to show/hide scroll-to-top button
  React.useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 300);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Scroll to top
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="section-padding bg-gradient-to-br from-primary-50 via-white to-accent-50 dark:from-neutral-900 dark:via-neutral-800 dark:to-neutral-900">
        <div className="container-width">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center lg:text-left"
            >
              <h1 className="text-4xl lg:text-6xl font-bold text-neutral-900 dark:text-neutral-100 mb-6">
                Fast & Accurate{' '}
                <span className="gradient-text">Chili Leaf Disease</span>{' '}
                Detection
              </h1>
              <p className="text-xl text-neutral-600 dark:text-neutral-400 mb-8 leading-relaxed">
                Advanced machine learning powered by ChiliFusionNet ensemble for 
                early detection and classification of chili plant diseases. 
                Revolutionizing smart agriculture with AI.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <button 
                  onClick={() => {
                    const testModelSection = document.getElementById('test-model');
                    testModelSection?.scrollIntoView({ behavior: 'smooth' });
                  }}
                  className="btn-primary"
                >
                  Try Demo
                  <ArrowRight className="ml-2 h-4 w-4" />
                </button>
                <Link to="/abstract" className="btn-secondary">
                  Learn More
                </Link>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="relative aspect-square rounded-3xl overflow-hidden shadow-2xl">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentImageIndex}
                    initial={{ opacity: 0, scale: 1.1 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 1, ease: "easeInOut" }}
                    className={`absolute inset-0 bg-gradient-to-br ${heroImages[currentImageIndex].color} flex items-center justify-center`}
                  >
                    <motion.img
                      src={heroImages[currentImageIndex].src}
                      alt={heroImages[currentImageIndex].label}
                      className="w-full h-full object-cover"
                      initial={{ scale: 1.1 }}
                      animate={{ scale: 1 }}
                      transition={{ duration: 1.2, ease: "easeOut" }}
                      onError={(e) => {
                        // Fallback to emoji if image fails to load
                        const target = e.target as HTMLImageElement;
                        target.style.display = 'none';
                        target.parentElement!.innerHTML = '<div class="text-6xl">🌶️</div>';
                      }}
                    />
                    
                    {/* Overlay with gradient for better text visibility */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent" />
                    
                    {/* Image info overlay */}
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.3 }}
                      className="absolute bottom-4 left-4 text-white"
                    >
                      <div className="text-sm font-semibold bg-black/30 backdrop-blur-sm px-3 py-1 rounded-lg">
                        {heroImages[currentImageIndex].label}
                      </div>
                    </motion.div>
                  </motion.div>
                </AnimatePresence>

                {/* Progress indicators */}
                <div className="absolute bottom-4 right-4 flex gap-2">
                  {heroImages.map((_, index) => (
                    <motion.button
                      key={index}
                      onClick={() => setCurrentImageIndex(index)}
                      className={`w-2 h-2 rounded-full transition-all duration-300 ${
                        index === currentImageIndex 
                          ? 'bg-white shadow-lg scale-125' 
                          : 'bg-white/50 hover:bg-white/75'
                      }`}
                      whileHover={{ scale: 1.2 }}
                      whileTap={{ scale: 0.9 }}
                    />
                  ))}
                </div>
              </div>

              {/* Floating cards */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="absolute -top-4 -right-4 bg-white dark:bg-neutral-800 p-4 rounded-2xl shadow-lg border border-neutral-200 dark:border-neutral-700"
              >
                <div className="text-sm font-semibold text-neutral-900 dark:text-neutral-100">96.32%</div>
                <div className="text-xs text-neutral-600 dark:text-neutral-400">Accuracy</div>
              </motion.div>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
                className="absolute -bottom-4 -left-4 bg-white dark:bg-neutral-800 p-4 rounded-2xl shadow-lg border border-neutral-200 dark:border-neutral-700"
              >
                <div className="text-sm font-semibold text-neutral-900 dark:text-neutral-100">6 Classes</div>
                <div className="text-xs text-neutral-600 dark:text-neutral-400">Diseases</div>
              </motion.div>
              
              {/* Additional floating info card for current image */}
              <motion.div
                key={`info-${currentImageIndex}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
                className="absolute top-4 left-4 bg-white/90 dark:bg-neutral-800/90 backdrop-blur-sm p-3 rounded-xl shadow-lg border border-neutral-200 dark:border-neutral-700"
              >
                <div className="text-xs font-medium text-neutral-900 dark:text-neutral-100">
                  {heroImages[currentImageIndex].description}
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section-padding">
        <div className="container-width">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">
              Why Choose ChiliFusionNet?
            </h2>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Our ensemble approach combines multiple machine learning algorithms 
              for superior accuracy and reliability in disease detection.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: Zap,
                title: 'Fast Detection',
                description: 'Get results in seconds with our optimized inference pipeline'
              },
              {
                icon: Shield,
                title: 'High Accuracy',
                description: 'Achieve 96.32%+ accuracy with our ensemble learning approach'
              },
              {
                icon: Brain,
                title: 'Smart Analysis',
                description: 'Uses pretrained feature extractors and ChiliFusionNet'
              },
              {
                icon: TrendingUp,
                title: 'Proven Results',
                description: 'Validated across multiple datasets with cross-validation'
              }
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="card-hover bg-white dark:bg-neutral-800 p-6 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-700"
              >
                <div className="p-3 rounded-xl bg-primary-100 dark:bg-primary-900 w-fit mb-4">
                  <feature.icon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                </div>
                <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-2">
                  {feature.title}
                </h3>
                <p className="text-neutral-600 dark:text-neutral-400">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Test Our Model Section */}
      <section id="test-model" className="bg-white dark:bg-neutral-900">
        <Demo />
      </section>

      {/* Authors Section */}
      <section id="authors" className="section-padding bg-neutral-50 dark:bg-neutral-800">
        <div className="container-width">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">
              Authors
            </h2>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Meet the researchers behind this innovative chili disease detection study
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                name: 'A.K.M. Fazlul Kobir Siam',
                role: 'B.Sc Student',
                description: 'Computer Science and Engineering, Daffodil International University',
                social: [
                  { icon: Linkedin, href: '#' },
                  { icon: Github, href: '#' },
                  { icon: Mail, href: '#' }
                ]
              },
              {
                name: 'Izaz Ahmmed Tuhin',
                role: 'B.Sc, Lecturer',
                description: 'Software Engineering, Daffodil International University',
                social: [
                  { icon: Linkedin, href: '#' },
                  { icon: Github, href: '#' },
                  { icon: Mail, href: '#' }
                ]
              },
              {
                name: 'Md Mahfuzur Rahman Shanto',
                role: 'B.Sc Student',
                description: 'Software Engineering, Daffodil International University',
                social: [
                  { icon: Linkedin, href: '#' },
                  { icon: Github, href: '#' },
                  { icon: Mail, href: '#' }
                ]
              },
              // {
              //   name: 'Md Rajib Mia',
              //   role: 'MSc, Lecturer (Senior Scale)',
              //   description: 'Software Engineering, Daffodil International University',
              //   social: [
              //     { icon: Linkedin, href: '#' },
              //     { icon: Github, href: '#' },
              //     { icon: Mail, href: '#' }
              //   ]
              // },
              // {
              //   name: 'Dr. Imran Mahmud',
              //   role: 'PhD, Professor',
              //   description: 'Software Engineering, Daffodil International University',
              //   social: [
              //     { icon: Linkedin, href: '#' },
              //     { icon: Github, href: '#' },
              //     { icon: Mail, href: '#' }
              //   ]
              // },
              // {
              //   name: 'Apurba Ghosh',
              //   role: 'MSc, Assistant Professor',
              //   description: 'Multimedia & Creative Technology, Daffodil International University',
              //   social: [
              //     { icon: Linkedin, href: '#' },
              //     { icon: Github, href: '#' },
              //     { icon: Mail, href: '#' }
              //   ]
              // }
            ].map((author, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white dark:bg-neutral-900 p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 text-center card-hover"
              >
                <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
                  <span className="text-2xl">👤</span>
                </div>
                <h3 className="text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-2">
                  {author.name}
                </h3>
                <p className="text-primary-600 dark:text-primary-400 font-medium mb-2">
                  {author.role}
                </p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
                  {author.description}
                </p>
                <div className="flex justify-center gap-3">
                  {author.social.map((social, socialIndex) => (
                    <a
                      key={socialIndex}
                      href={social.href}
                      className="w-8 h-8 bg-neutral-100 dark:bg-neutral-800 rounded-full flex items-center justify-center hover:bg-primary-100 dark:hover:bg-primary-900 transition-colors"
                    >
                      <social.icon className="h-4 w-4 text-neutral-600 dark:text-neutral-400" />
                    </a>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-primary-600 dark:bg-primary-800">
        <div className="container-width text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              Ready to Detect Chili Diseases?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Upload your chili leaf images and get instant disease classification 
              with confidence scores and visual explanations.
            </p>
            <Link 
              to="/demo" 
              className="inline-flex items-center justify-center rounded-xl bg-white px-8 py-4 text-lg font-semibold text-primary-600 shadow-sm transition-all hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-primary-600"
            >
              Start Detection
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Scroll to Top Button */}
      {showScrollTop && (
        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          onClick={scrollToTop}
          className="fixed bottom-8 right-8 z-50 w-12 h-12 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg transition-colors flex items-center justify-center"
          aria-label="Scroll to top"
        >
          <ChevronUp className="h-6 w-6" />
        </motion.button>
      )}
    </div>
  );
};
