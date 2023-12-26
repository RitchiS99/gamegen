const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    context: __dirname,
    entry: {
        app: "./assets/js/app.js",
    },
    output: {
        path: path.resolve("./assets/dev/"),
        filename: "[name].bundle.js",
    },
    plugins: [
        new BundleTracker({ filename: "./webpack-stats.dev.json" }),
        new MiniCssExtractPlugin({
            filename: "[name].bundle.css",
        }),
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
                loader: "esbuild-loader",
                options: {
                    target: "firefox91",
                },
            },
        ],
    },
};

