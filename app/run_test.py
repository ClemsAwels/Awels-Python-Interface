import unittest

if __name__ == '__main__':
    # Spécifiez le chemin du fichier de test
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir='test', pattern='test_*.py')
    
    # Exécutez les tests
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)