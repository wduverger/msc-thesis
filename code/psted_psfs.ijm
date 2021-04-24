// open("../data/2021-04-21 - 2 psted psfs.msr");

// Close unnessecary images
selectWindow("2 psted psfs.msr - beads_STED_align {4} [Pop]");  close();
selectWindow("2 psted psfs.msr - beads_561_align {4} [Pop]");   close();
selectWindow("2 psted psfs.msr - beads_STED_align {4}");        close();
selectWindow("2 psted psfs.msr - beads_640_align {4}");         close();
selectWindow("2 psted psfs.msr - beads_561_align {4}");         close();
selectWindow("2 psted psfs.msr - beads_STED_align {1}");        close();
selectWindow("2 psted psfs.msr - beads_640_align {1}");         close();
selectWindow("2 psted psfs.msr - beads_561_align {1}");         close();

// Create a 3-colour stack
run("Images to Stack", "name=561 title=561 use");
run("Images to Stack", "name=640 title=640 use");
run("Images to Stack", "name=775 title=STED use");
run("Merge Channels...", "c1=775 c2=640 c3=561 create");

// Duplicate and threshold it
run("Duplicate...", "duplicate");
run("Convert to Mask", "method=Moments background=Dark calculate black");
run("Dilate", "stack");

// `redirect=Composite` will use intensity values from stack
run("Set Measurements...", "area min centroid fit integrated stack redirect=Composite decimal=3");
run("Analyze Particles...", "  show=Ellipses display exclude clear stack");
// saveAs("Results", "data/psted_psfs.csv");

selectWindow("Composite-1");
run("MTrack2 ", "minimum=1 maximum=999999 maximum_=10 minimum_=2 show_0 show_1");

// saveAs("Results", "data/psted_psfs_tracks.csv");