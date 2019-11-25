# UV_Straightener
Script for straightening Maya UV`s



For many years of using Maya I reached the point that I got tired of my rigid uvs straightening workflow. Encountered much better uvs straightening methods on 3dsmax, Unfold3d, Blender I wanted to bring something similar in Maya.  Therefore I started thinking about how without going deep into Maya API and recreating complex algorithms I could create a script that would facilitate my workflow. I started experimenting and thought about idea to create custom pinning script that would:

-straighten selected uvs by putting them either on vertical axis line or horizontal

-marking them accordingly  in UV editor by creating shader and applying textures for every separate marked line

-unfolding marked uvs accordingly in a vertical or horizontal manner

-unfolding rest marked shell uvs excluding marked uvs

To put it simply the idea was to make custom pinning tool with a function to move pinned uvs and unfold them. 
In the process of making and releasing prototype version, I faced a couple of problems like limitation of uv editor texture representation in UDIMs space, slow calculation process ( if you have enormous amount of marked lines ). Although those problems can be ignored by limiting yourself with working just in one to one uvs space and working only with one uv shell at the time. There are plenty of space for improvements and fixes left although I made this script for test and learning process. To create a proper uv straightener might be better solution to go deeper on Maya`s API and building faster and more efficient marking system which would not rely on textures.


Here is how this script works visually:

<a href="https://gifyu.com/image/v4F8"><img src="https://s5.gifyu.com/images/UV_Straightener_ALPHA_explolder.gif" alt="UV_Straightener_ALPHA_explolder.gif" border="0" /></a>
