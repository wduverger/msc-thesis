% This class provides an unofficial alternative to the original TU Delft
% template for reports. It features a redesigned cover page and a
% rewritten class file for easier customization.
%
% Rewritten template by Daan Zwaneveld. Original template by TU Delft
% (available here: https://www.tudelft.nl/huisstijl/downloads/).
%
% This template is available under CC BY-NC 4.0. For more information,
% see https://creativecommons.org/licenses/by-nc/4.0/. No attribution
% is required in reports created using this template.

%% Class is based on the default book class and options will be passed
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mystyle}[06-02-2021 v1.3.1 TU Delft Report Class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[10pt,oneside]{book}

%% Main packages in the document
\RequirePackage{amsmath}    % Mathematics
\RequirePackage{amssymb}    % Symbols
\RequirePackage{siunitx}    % Various functions, e.g. \num{}

\RequirePackage{tabularx}   % Additional functions to tables
\RequirePackage{booktabs}   % Adds more line functionality to tables
\RequirePackage{longtable}  % Lets tables break over page
\RequirePackage{multirow}   % Counterpart of multi columns
\RequirePackage{enumitem}   % Customise the list spacing

\RequirePackage{geometry}   % Document geometry
\RequirePackage{titlesec}   % Custom titles
\RequirePackage{titletoc}   % Custom table of contents
\RequirePackage{fancyhdr}   % Custom header/footer
\RequirePackage[hyphens]{url}
\RequirePackage[hidelinks]{hyperref} % Improved referencing/links
\RequirePackage[numbers,sort&compress]{natbib}


\RequirePackage{graphicx}   % Adding images
\RequirePackage{float}      % Additional float parameters
\RequirePackage[labelfont=bf,justification=centering,footnotesize]{caption} % Captions
\RequirePackage{subcaption} % Subfigures and subcaptions
\RequirePackage{xcolor}     % Using colours in documents
\RequirePackage{tikz}       % Create graphic elements

\RequirePackage{datetime}   % Used in preface for monthname
\RequirePackage{microtype}  % Refinements towards typographical perfection
\RequirePackage[numbib, nottoc]{tocbibind} % Add the lists to the table of contents
\RequirePackage{xspace}     % Ensures correct spacing after macros like \deg
\RequirePackage{etoolbox}   % General toolbox (e.g. \ifdefvoid)

% Extra packages
\usepackage{physics, tabularx, mathtools, titling}

%%%%% 1. General Definitions for the Document and Bibliography %%%%%

%% Commands to define the title, author, etc
\renewcommand{\title}[1]{%
    \def\@title{#1}%
    \hypersetup{pdftitle=#1} % Adds it to metadata
	\def\thetitle{#1}
}

\renewcommand*\author[1]{%
    \def\@author{#1}%
    \hypersetup{pdfauthor=#1} % Adds it to metadata
    \def\theauthor{#1}
}

\newcommand*\subtitle[1]{\def\@subtitle{#1}}
\newcommand*\coverimage[1]{\def\@cover@image{#1}}
\newcommand\subject[1]{\def\@subject{#1}}

%% Scaling the margins to be slightly smaller than default (25mm)
\geometry{a4paper,margin=25mm}

%% Reducing white space in lists slightly (both enumerate and itemize)
\setlist{itemsep=-2pt}

%% Setting up \autoref to use uppercase
\def\sectionautorefname{Section}
\def\chapterautorefname{Chapter}
\let\subsectionautorefname\sectionautorefname
\let\subsubsectionautorefname\sectionautorefname

%% Bibliography settings
%\RequirePackage[backend=bibtex]{biblatex}  % Manage bibliography
%\setlength\bibitemsep{0.7\itemsep} % More spacing to improve readability
%\setcounter{biburlnumpenalty}{7000} % Prevent urls running into margins in bibliography
%\setcounter{biburllcpenalty}{7000}
%\setcounter{biburlucpenalty}{7000}

%%%%% 2. Loading all the Fonts (Supports pdfLaTeX, XeLaTeX and LuaLaTeX) %%%%%
\RequirePackage{fontspec} % Custom fonts

%% Adding the various fonts
%\setmainfont{Latin Modern Roman} % Xetex sets these fonts by default!
%\setmathsf{Latin Modern Roman}
\setmathtt[Path=layout/]{TUDelft-UltraLight.ttf}

\newfontfamily\tudtitlefamily[Path=layout/]{TUDelft-UltraLight.ttf}
\newfontfamily\garamondfont[Path=layout/]{Adobe Garamond Pro Semibold.otf}
\newfontfamily\frutigerfont[Path=layout/]{FrutigerLTStd-Roman.otf}
\newfontfamily\frutigerbold[Path=layout/]{FrutigerLTStd-Bold.otf}
%\newfontfamily\quotefont{Georgia}

%% Defining commands to be used in layout
\def\largetitlestyle{\tudtitlefamily}
\def\titlestyle{\garamondfont}

%% Changing the quote environment to use Georgia
\AtBeginEnvironment{quote}{\quotefont}

%%%%% 3. Adjusting the Titles in Text and Table of Contents %%%%%

%% Formatting chapter titles and spacing
\titleformat{\chapter}[display]
    {\flushright}
    {\fontsize{96}{96}\largetitlestyle\thechapter}
    {0pt}
    {\Huge\titlestyle}
\titlespacing*{\chapter}{0pt}{0pt}{2\baselineskip}

%% Formatting section titles and spacing
\titleformat{\section}
    {\Large\titlestyle}
    {\thesection.}
    {5pt}
    {}
\titlespacing*{\section}{0pt}{\baselineskip}{0pt}

%% Formatting subsections titles and spacing
\titleformat{\subsection}
    {\large\titlestyle}
    {\thesubsection.}
    {5pt}
    {}
\titlespacing*{\subsection}{0pt}{\baselineskip}{0pt}

%% Formatting subsubsections titles and spacing
\titleformat{\subsubsection}
    {\titlestyle\bfseries}
    {}
    {0pt}
    {}
\titlespacing*{\subsubsection}{0pt}{\bigskipamount}{0pt}

%% Changing font and spacing in the table of contents
\dottedcontents{chapter}[1.5em]{\vspace{0.5\baselineskip}\titlestyle}{1.5em}{0pc}
\dottedcontents{section}[3.8em]{\titlestyle}{2.3em}{8pt}
\dottedcontents{subsection}[7em]{\titlestyle}{3.2em}{8pt}

%%%%% 4. Adjusting the Header and Footer %%%%%

%% Adding a head rule to pages
\renewcommand*\headrule{%
    {\hrule\@height\headrulewidth\@width\headwidth}%
    \vskip-\headrulewidth}

%% Page style for title pages
\fancypagestyle{plain}{%
    \fancyhf{}
    \renewcommand*\headrulewidth{0pt}
    \fancyfoot[C]{\thepage}}

%% Fancy style for the main matter, depends on oneside/twoside option
\if@twoside%
    \fancyhf{}
    \fancyhead[LE,RO]{\titlestyle\thepage}
    \fancyhead[RE]{\titlestyle\nouppercase{\leftmark}}
    \fancyhead[LO]{\titlestyle\nouppercase{\rightmark}}
    \RequirePackage{emptypage} % Clears empty pages
\else%
    \fancyhf{}
    \fancyhead[R]{\titlestyle\thepage}
    \fancyhead[L]{\titlestyle\nouppercase{\rightmark}}
\fi

\pagestyle{fancy} % Setting it to default

%%%%% 5. My own extra commands %%%%%

% Commands for inline comments
\definecolor{green}{rgb}{0.17,0.68,0.11}
\definecolor{orange}{rgb}{0.8,0.4,0.1}
\newcommand{\question}[1]{\textcolor{green}{(#1)}}
\newcommand{\todo}[1]{\textcolor{orange}{(#1)}}
\newcommand{\todolist}[1]{
	\textcolor{orange}{
		To do:
		\begin{itemize}#1\end{itemize}
	}
}