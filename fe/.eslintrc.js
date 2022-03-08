module.exports = {
    extends: ['plugin:vue/vue3-essential', 'prettier'],
    parserOptions: {
        ecmaVersio: 12,
        sourceType: 'module',
        parser: '@typescript-eslint/parser',
    },
    plugins: ['vue', '@typescript-eslint'],
}
