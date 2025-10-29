import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Moon, Sun, Menu, X, Leaf, Github, FileText, ChevronDown } from 'lucide-react';

interface NavbarProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ darkMode, toggleDarkMode }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [activeSection, setActiveSection] = React.useState('');
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/abstract', label: 'Abstract' },
    { path: '/#test-model', label: 'Demo' },
    { path: '/#authors', label: 'Authors' },
  ];

  // Track active section based on scroll position
  React.useEffect(() => {
    if (location.pathname !== '/') {
      setActiveSection('');
      return;
    }

    const handleScroll = () => {
      const sections = ['test-model', 'authors'];
      const scrollPosition = window.scrollY + 100; // Offset for better detection

      for (const sectionId of sections) {
        const element = document.getElementById(sectionId);
        if (element) {
          const rect = element.getBoundingClientRect();
          const elementTop = window.scrollY + rect.top;
          const elementBottom = elementTop + rect.height;

          if (scrollPosition >= elementTop && scrollPosition < elementBottom) {
            setActiveSection(sectionId);
            return;
          }
        }
      }
      
      // If not in any specific section, clear active section
      setActiveSection('');
    };

    handleScroll(); // Check initial position
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [location.pathname]);

  const isActive = (path: string) => location.pathname === path;

  const isAnchorActive = (path: string) => {
    if (path === '/#test-model') return activeSection === 'test-model';
    if (path === '/#authors') return activeSection === 'authors';
    return false;
  };

  const handleNavClick = (path: string) => {
    if (path === '/#authors') {
      if (location.pathname === '/') {
        // If already on home page, scroll to authors section
        const authorsSection = document.getElementById('authors');
        authorsSection?.scrollIntoView({ behavior: 'smooth' });
      } else {
        // If on different page, navigate to home then scroll
        window.location.href = '/#authors';
      }
    } else if (path === '/#test-model') {
      if (location.pathname === '/') {
        // If already on home page, scroll to test model section
        const testModelSection = document.getElementById('test-model');
        testModelSection?.scrollIntoView({ behavior: 'smooth' });
      } else {
        // If on different page, navigate to home then scroll
        window.location.href = '/#test-model';
      }
    }
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-neutral-200 dark:border-neutral-700 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md">
      <div className="container-width section-padding py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="p-2 rounded-xl bg-primary-100 dark:bg-primary-900 group-hover:bg-primary-200 dark:group-hover:bg-primary-800 transition-colors">
              <Leaf className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            </div>
            <span className="text-xl font-bold text-neutral-900 dark:text-neutral-100">
              Chili<span className="gradient-text">FusionNet</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-8">
            {navItems.map((item) => (
              item.path === '/#authors' || item.path === '/#test-model' ? (
                <button
                  key={item.path}
                  onClick={() => handleNavClick(item.path)}
                  className={`text-sm font-medium transition-colors hover:text-primary-600 dark:hover:text-primary-400 relative ${
                    isAnchorActive(item.path)
                      ? 'text-primary-600 dark:text-primary-400'
                      : 'text-neutral-600 dark:text-neutral-400'
                  }`}
                >
                  {item.label}
                  {isAnchorActive(item.path) && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="absolute -bottom-1 left-0 right-0 h-0.5 bg-primary-600 dark:bg-primary-400"
                      initial={false}
                      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    />
                  )}
                </button>
              ) : (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`text-sm font-medium transition-colors hover:text-primary-600 dark:hover:text-primary-400 ${
                    isActive(item.path)
                      ? 'text-primary-600 dark:text-primary-400'
                      : 'text-neutral-600 dark:text-neutral-400'
                  }`}
                >
                  {item.label}
                  {isActive(item.path) && (
                    <motion.div
                      layoutId="navbar-indicator"
                      className="mt-1 h-0.5 w-full bg-primary-600 dark:bg-primary-400"
                      initial={false}
                      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    />
                  )}
                </Link>
              )
            ))}
          </div>

          {/* Controls */}
          <div className="flex items-center space-x-4">
            {/* GitHub Link */}
            <a
              href="https://github.com/mahfuzswe/ChiliFusionNet"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-xl bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors focus-visible"
              aria-label="View on GitHub"
              title="View on GitHub"
            >
              <Github className="h-5 w-5 text-neutral-600 dark:text-neutral-400" />
            </a>

            {/* Paper Link */}
            <a
              href="/paper.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-xl bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors focus-visible"
              aria-label="Read Paper"
              title="Read Paper"
            >
              <FileText className="h-5 w-5 text-neutral-600 dark:text-neutral-400" />
            </a>

            {/* Dark Mode Toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-xl bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors focus-visible"
              aria-label="Toggle dark mode"
            >
              {darkMode ? (
                <Sun className="h-5 w-5 text-neutral-600 dark:text-neutral-400" />
              ) : (
                <Moon className="h-5 w-5 text-neutral-600 dark:text-neutral-400" />
              )}
            </button>

            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="lg:hidden p-2 rounded-xl bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors focus-visible"
              aria-label="Toggle mobile menu"
            >
              {isOpen ? (
                <X className="h-5 w-5 text-neutral-600 dark:text-neutral-400" />
              ) : (
                <Menu className="h-5 w-5 text-neutral-600 dark:text-neutral-400" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden mt-4 pt-4 border-t border-neutral-200 dark:border-neutral-700"
          >
            <div className="flex flex-col space-y-3">
              {navItems.map((item) => (
                item.path === '/#authors' || item.path === '/#test-model' ? (
                  <button
                    key={item.path}
                    onClick={() => {
                      setIsOpen(false);
                      handleNavClick(item.path);
                    }}
                    className={`py-2 px-3 rounded-xl text-sm font-medium transition-colors text-left ${
                      isAnchorActive(item.path)
                        ? 'bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400'
                        : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800'
                    }`}
                  >
                    {item.label}
                  </button>
                ) : (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setIsOpen(false)}
                    className={`py-2 px-3 rounded-xl text-sm font-medium transition-colors ${
                      isActive(item.path)
                        ? 'bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400'
                        : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800'
                    }`}
                  >
                    {item.label}
                  </Link>
                )
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </nav>
  );
};
