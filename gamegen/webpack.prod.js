const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')
// const { ESBuildMinifyPlugin } = require('esbuild-loader')

module.exports = {
    context: __dirname,
    entry: {
        app: "./assets/js/app.js",
    },
    output: {
        path: path.resolve('./assets/dist/'),
        filename: "[name].[contenthash].bundle.js"
    },
    optimization: {
        splitChunks: {
            chunks: 'all',
        },
        minimizer: [
            new CssMinimizerPlugin(),
            // new ESBuildMinifyPlugin({target: "firefox91"})
        ],
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json', relativePath: true}),
        new MiniCssExtractPlugin({
            filename: "[name][contenthash].css"
        })
    ],
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "postcss-loader",
                    "sass-loader",
                ],
            },
            {
                test: /\.js$/,
                loader: 'esbuild-loader',
                options: {
                    target: 'firefox91'
                }
            }
        ]
    },
}
