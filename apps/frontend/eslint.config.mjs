import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import prettier from 'eslint-config-prettier';

export default tseslint.config(
  // Ignore build artifacts and generated files
  {
    ignores: [
      '.next/**',
      'out/**',
      'dist/**',
      'build/**',
      'node_modules/**',
      '.vercel/**',
      'coverage/**',
      '*.config.js',
      'next-env.d.ts',
    ]
  },

  eslint.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    plugins: {
      react,
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
    },

    settings: {
      react: {
        version: 'detect'
      }
    },

    rules: {
      // ═══════════════════════════════════════════════════════
      // PILAR 1: PUREZA OPERATIVA
      // "Máxima verdad en mínima forma"
      // ═══════════════════════════════════════════════════════

      'max-lines': ['warn', {
        max: 300,
        skipBlankLines: true,
        skipComments: true
      }],

      'max-lines-per-function': ['warn', {
        max: 50,
        skipBlankLines: true,
        skipComments: true
      }],

      'complexity': ['warn', 10],

      'max-depth': ['warn', 4],

      'max-params': ['warn', 4],

      // ═══════════════════════════════════════════════════════
      // PILAR 3: RESPONSABILIDAD CONSCIENTE
      // "Propiedad total sobre código"
      // ═══════════════════════════════════════════════════════

      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_'
      }],

      '@typescript-eslint/no-explicit-any': 'error',

      '@typescript-eslint/explicit-function-return-type': ['warn', {
        allowExpressions: true,
        allowTypedFunctionExpressions: true
      }],

      'no-console': ['warn', {
        allow: ['warn', 'error', 'info']
      }],

      'no-debugger': 'error',

      'no-alert': 'warn',

      // ═══════════════════════════════════════════════════════
      // PILAR 4: EXPRESIÓN AUTÉNTICA
      // "Código que expresa intención clara"
      // ═══════════════════════════════════════════════════════

      'prefer-const': 'error',

      'no-var': 'error',

      'object-shorthand': ['warn', 'always'],

      'prefer-template': 'warn',

      'prefer-arrow-callback': 'warn',

      // ═══════════════════════════════════════════════════════
      // PILAR 5: IMPLEMENTACIÓN TÉCNICA
      // "React/Next.js best practices"
      // ═══════════════════════════════════════════════════════

      'react/react-in-jsx-scope': 'off', // Next.js auto-imports

      'react/prop-types': 'off', // TypeScript handles this

      'react-hooks/rules-of-hooks': 'error',

      'react-hooks/exhaustive-deps': 'warn',

      'react/jsx-no-target-blank': 'error',

      'react/jsx-key': 'error',

      'react/no-unescaped-entities': 'warn',

      // ═══════════════════════════════════════════════════════
      // PILAR 6: CONTRIBUCIÓN ECOSISTÉMICA
      // "Accesibilidad como responsabilidad"
      // ═══════════════════════════════════════════════════════

      'jsx-a11y/alt-text': 'error',

      'jsx-a11y/anchor-is-valid': 'warn',

      'jsx-a11y/click-events-have-key-events': 'warn',

      'jsx-a11y/no-static-element-interactions': 'warn',

      // Para experiencia inmersiva, permitir algunos patterns
      'jsx-a11y/no-autofocus': 'off', // Estado Cero necesita focus

      // ═══════════════════════════════════════════════════════
      // PILAR 8: EVOLUCIÓN CONTINUA
      // "Prevenir deprecated code"
      // ═══════════════════════════════════════════════════════

      '@typescript-eslint/no-deprecated': 'warn',

      'no-restricted-imports': ['error', {
        patterns: [
          {
            group: ['../*'],
            message: 'Use absolute imports (@/) instead of relative parent imports'
          }
        ]
      }],
    },

    languageOptions: {
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // Configuración específica para Estado Cero inmersivo
  {
    files: ['**/estado-cero/**/*.tsx', '**/estado-cero/**/*.ts'],
    rules: {
      // Permitir funciones más largas (animaciones complejas)
      'max-lines-per-function': ['warn', { max: 100 }],

      // Permitir complejidad mayor (3D interactions)
      'complexity': ['warn', 15],

      // Los componentes 3D pueden ser más largos
      'max-lines': ['warn', { max: 500 }],
    }
  },

  prettier, // Disable formatting rules
);
