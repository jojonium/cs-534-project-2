CS 534 Project 2

## Set up

First, install Node.js and npm if you haven't already. Then install all the
dependencies of the project:

```
$ npm install
```

Write TypeScript in the `src` directory. HTML and CSS are served from the
`static` directory. To compile the TypeScript and bundle it into
`static/bundle.js`, do:

```
$ npm run build
```

Then, start serving the compiled content with:

```
$ npm run start
```

If you open `http://localhost:3000` in a browser you should see a page that
says the TypeScript was successfully compiled.

You can also run the TypeScript compiler in "watch" mode, so that it will
automatically recompile as source files are changed with:

```
$ npm run watch
```

This command also starts the server, so you can instantly view the compiled
result in a browser.

### Code style

`eslint` and `prettier` are already set up, and should work with most IDEs and
text editors. You can set up VSCode and other editors to automatically format
your source files when they are saved.  The TypeScript compiler should give you
warnings and errors for bad code formatting. You can also run `npm run lint` to
fix formatting in all source files. This command will be run automatically when
you `npm run build` as well.
