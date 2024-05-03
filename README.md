# EasyAlign plugin for Glaxnimate

This plugin adds some missing alignment features to Glaxnimate:

+ Setting the anchor point to the center, any of the corners or the middle of an edge
+ Setting a target element and align another element relative to that target

Current limitaions:

+ Text elements can't be supported at the moment. Just convert the text to a path and
  everything works as expected. If you still need the text element you can duplicate it
  before converting it to a path and delete the copy after alignment.
+ Precompositions only work correctly when their timing is not stretched or compressed
  in any way because there is currently no way to measure the correct position and size
  in such cases.
