"""Build the six tutorial readers from their existing examples and a shared layout.

First import: --original-directory PATH (a backup of the six original HTML pages).
Subsequent builds use the checked-in examples in assets/code/tutorials/.
"""
from pathlib import Path
from html import escape, unescape
import argparse
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / 'pages/tutorial_pages'
CODE = ROOT / 'assets/code/tutorials'
VERSION = '20261008-reader86'

def section(title, description, filename=None, original=None, images=(), note='', body=''):
    return dict(title=title, description=description, filename=filename, original=original,
                images=list(images), note=note, body=body)

GUIDES = [
    dict(id='rs_data_processing', title='Read & write GeoTIFF', category='Geospatial',
         intro='Move between georeferenced raster files and NumPy arrays while keeping the spatial metadata intact.',
         tags=['Python', 'GDAL', 'NumPy'], level='Python basics', flow=['GeoTIFF', 'NumPy array', 'GeoTIFF'],
         goals=['Read raster values and spatial metadata.', 'Write multiband arrays back to a GeoTIFF.', 'Check array shape, coordinate system, and geotransform.'],
         prep=['A Python environment with NumPy and GDAL.', 'A local GeoTIFF for the usage example.', 'Arrays use rows × columns × bands; a single band needs a band axis.'],
         sections=[
             section('Read & write helpers', 'The reader returns the array, geotransform, projection, and raster dimensions. The writer expects a three-dimensional array and writes Float32 bands.', 'read_write_geotiff.py', 0,
                     body='<dl class="lesson-definitions"><div><dt>Array shape</dt><dd>Multiband reads are rearranged from bands × rows × columns to rows × columns × bands.</dd></div><div><dt>Spatial metadata</dt><dd>Pass the original geotransform and projection to the writer to retain the raster location.</dd></div></dl>'),
             section('Use the helpers', 'Save the helpers above as read_write_geotiff.py, place a raster in your data folder, and replace the input and output filenames.', 'geotiff_usage.py',
                     note='A single-band read returns a 2D array. Add the final band dimension before calling the writer.'),
             section('Check the output', 'After writing, inspect the output alongside the input. A matching array shape alone does not confirm that the coordinates were retained.',
                     body='<ul class="lesson-checklist"><li>Confirm rows, columns, and band count.</li><li>Compare the projection and six geotransform values.</li><li>Check data type and NoData behavior for your analysis.</li><li>Reopen the output and compare raster values.</li></ul>')],
         resources=[('GDAL raster API', 'https://gdal.org/en/stable/api/python/raster_api.html')]),
    dict(id='data_visualization', title='Python for data visualization', category='Visualization',
         intro='Build clear scientific figures with deliberate subplot layouts, readable axes, and compact legends.',
         tags=['Python', 'Matplotlib', 'Figure design'], level='Python basics', hero='./data_visualization_image/1.3.png',
         goals=['Choose a layout for single and multipanel figures.', 'Control axes, ticks, grids, and shared labels.', 'Place and customize legends.'],
         prep=['Python and Matplotlib.', 'The layout examples use empty axes; no dataset is needed.', 'The legend snippet continues an existing plot with ax and legend handles.'],
         sections=[
             section('Create axes with subplots', 'Start with a single axis or a regular grid. Shared figure labels are useful when several panels use the same variables.', 'subplots.py', 0,
                     images=[('./data_visualization_image/1.1.1.png','Single axis'),('./data_visualization_image/1.1.2.png','A 2 × 2 grid'),('./data_visualization_image/1.1.3.png','Shared figure labels')],
                     note='A 2 × 2 axes array is indexed as ax[row, column]. Use ax.ravel() when you want to iterate over individual panels.'),
             section('Build panels with figure', 'Create the figure first, then add each panel in a loop. This is useful when panel creation is part of an iterative workflow.', 'figure_panels.py', 1,
                     images=[('./data_visualization_image/1.2.1.png','Default figure background'),('./data_visualization_image/1.2.2.png','Custom figure background')]),
             section('Arrange panels with GridSpec', 'Use a grid to make panels span different numbers of rows or columns. The example arranges four panels across a flexible grid.', 'gridspec_layout.py', 2,
                     images=[('./data_visualization_image/1.3.png','Four panels arranged with GridSpec')]),
             section('Style axes and ticks', 'Set labels and limits, format tick values, control spines, and use a light grid to guide the reader without distracting from the data.', 'axes_style.py', 3,
                     images=[('./data_visualization_image/2.1.png','Axis labels, ticks, and grid settings')]),
             section('Refine the legend', 'Control placement, columns, spacing, and marker appearance. Run this snippet after creating the plotted series and their legend labels.', 'legend_style.py', 4,
                     note='This example uses ax and original_handle_colors from the surrounding plotting workflow. It is a continuation snippet.')],
         resources=[('Matplotlib tutorials','https://matplotlib.org/stable/tutorials/index.html'),('GridSpec reference','https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html')]),
    dict(id='scatter_line_plot', title='Scatter & line plots', category='Visualization',
         intro='Explore model performance, trait relationships, seasonal patterns, and uncertainty with research plotting examples.',
         tags=['Python', 'Matplotlib', 'Seaborn'], level='Plotting experience', hero='./data_visualization_image/random_temporal_cv.jpg',
         goals=['Show observation–prediction agreement and point density.', 'Compare trait distributions and relationships.', 'Visualize seasonal changes, groups, and model performance.'],
         prep=['NumPy, pandas, SciPy, Matplotlib, and Seaborn.', 'Research examples require their project-specific CSV or MATLAB inputs.', 'Replace data and export paths. The input datasets are not bundled here.'],
         sections=[
             section('Prediction–observation scatter', 'Compare random and temporal cross-validation using density-colored points, a 1:1 line, uncertainty bars, and model metrics.', 'prediction_scatter.py', 0, images=[('./data_visualization_image/random_temporal_cv.jpg','Trait prediction under random and temporal cross-validation')], note='The reported metric values belong to the original study. Calculate new metrics when adapting this figure to another dataset.'),
             section('Trait covariance', 'Use a pair plot to compare trait distributions and relationships across plant functional types.', 'trait_covariance.py', 1, images=[('./data_visualization_image/trait_covariance.png','Covariance of plant traits across functional types')]),
             section('Density scatter comparisons', 'Combine multiple inputs in a panel layout and show the concentration of observations using a density-based color scale.', 'density_comparison.py', 2, images=[('./data_visualization_image/LAI_FRAR.jpg','Density scatter comparisons')]),
             section('Seasonal variation', 'Plot repeated trait observations through time and keep colors, labels, and date formatting consistent across panels.', 'seasonal_variation.py', 3, images=[('./data_visualization_image/seasonal_variation.png','Seasonal variation of plant traits')]),
             section('Functional-type extrapolation', 'Compare measurements and predictions across plant functional types with shared plotting settings.', 'functional_type_extrapolation.py', 4, images=[('./data_visualization_image/PFT_extra.png','Plant functional-type extrapolation')]),
             section('Trait variability', 'Combine grouped comparisons into a multipanel figure to summarize variation across traits and plant groups.', 'trait_variability.py', 5, images=[('./data_visualization_image/leaf_traits_variation.jpg','Variation in leaf traits')]),
             section('Model comparisons', 'Arrange model evaluation results in a consistent figure and keep labels, statistical annotations, and panel spacing readable.', 'model_comparison.py', 6, images=[('./data_visualization_image/pre-train_dnn.jpg','Model comparison figure')])],
         resources=[('Seaborn plotting functions','https://seaborn.pydata.org/api.html'),('Matplotlib tutorials','https://matplotlib.org/stable/tutorials/index.html')]),
    dict(id='global_forest_edge_mapping', title='Global forest-edge mapping', category='Geospatial',
         intro='Visualize global forest edges, summarize changes across regions, and connect edge dynamics with forest landscape patterns.',
         tags=['Python', 'Cartopy', 'Forest landscapes'], level='Geospatial experience', hero='./data_visualization_image/22_Forest edge dynamics statistics.jpg',
         goals=['Map forest-edge patterns with geographic context.', 'Compare edge changes across countries and time periods.', 'Explore edge–area relationships and landscape differences.'],
         prep=['GDAL, NumPy, pandas, SciPy, Matplotlib, Seaborn, and Cartopy; some examples also use GeoPandas and xarray.', 'Provide the raster and country-level tables referenced in each example.', 'Original research inputs are not bundled. Replace the project-specific paths.'],
         sections=[
             section('Map global forest edges', 'Read the raster, build geographic coordinates, and combine a global map with latitude and longitude summaries.', 'global_edge_map.py', 0, images=[('./data_visualization_image/11_Forest edge.jpg','Global forest-edge patterns and geographic summaries')]),
             section('Summarize changes by country', 'Link country statistics to continents and compare forest-edge changes in selected countries using a coordinated panel layout.', 'country_edge_statistics.py', 1, images=[('./data_visualization_image/22_Forest edge dynamics statistics.jpg','Country-level forest-edge dynamics')]),
             section('Visualize edge dynamics', 'Combine geospatial inputs and statistical panels to show the spatial and temporal structure of forest-edge change.', 'edge_dynamics.py', 2, images=[('./data_visualization_image/33_Forest edge dynamics.jpg','Spatial and temporal forest-edge dynamics')]),
             section('Relate edges to forest area', 'Explore the relationship between forest-edge length and forest area, with consistent axes and statistical annotations.', 'edge_area_relationships.py', 3, images=[('./data_visualization_image/44_forest edge_area relationships.jpg','Forest-edge and forest-area relationships')]),
             section('Compare landscape patterns', 'Compare forest landscape patterns across countries and connect the results with broader geographic differences.', 'landscape_patterns.py', 4, images=[('./data_visualization_image/55_unequal development of forest landscape patterns.jpg','Differences in forest landscape patterns')])],
         resources=[('Related forest-edge research','../research.html#dir-2'),('Cartopy documentation','https://cartopy.readthedocs.io/stable/'),('Related publication','https://doi.org/10.1038/s41467-026-78347-6')]),
    dict(id='hpc', title='Research computing with HPC & HTC', category='Computing',
         intro='A practical route from your local terminal to a configured environment, a submitted job, and readable results at UW–Madison CHTC.',
         tags=['Shell', 'Slurm', 'HTCondor'], level='Terminal basics', flow=['Connect', 'Submit', 'Monitor'],
         goals=['Choose between tightly coupled and independent workloads.', 'Connect, move files, and prepare a Python environment.', 'Submit and monitor a Slurm job.'],
         prep=['An approved CHTC account and its assigned access point.', 'A terminal on macOS, Linux, or Windows with SSH support.', 'Adjust paths, resource requests, and environment names for your project.'],
         sections=[
             section('Choose a computing system', 'Match the computing system to how your tasks communicate, rather than choosing by job size alone.',
                     body='<div class="lesson-comparison"><div><h4>HPC · Slurm</h4><p>Tightly coupled computations that coordinate work across nodes, such as MPI applications.</p></div><div><h4>HTC · HTCondor</h4><p>Many independent jobs, such as parameter sweeps or separate model runs.</p></div></div><p>Resource limits depend on the system and partition. Use the current <a href="https://chtc.cs.wisc.edu/uw-research-computing/hpc-overview" target="_blank" rel="noopener noreferrer">CHTC system overview ↗</a> for limits and policies.</p>'),
             section('Connect and transfer files', 'Use the access point in your welcome email. The HPC example below uses the currently documented spark-login host.', 'connect_and_transfer.sh',
                     note='Run SSH and SCP commands from your local terminal. For HTC, use the assigned ap2001 or ap2002 access point.',
                     body='<p>For an editor-based workflow, see <a href="https://code.visualstudio.com/docs/remote/ssh-tutorial" target="_blank" rel="noopener noreferrer">VS Code Remote SSH ↗</a>.</p>'),
             section('Prepare a Python environment', 'For the HPC example, use a Conda installation available to your compute job, then create a named environment with the packages your analysis needs.', 'python_environment.sh', images=[('hpc_image/miniconda_installation.png','Original Miniconda installation example')],
                     note='The screenshot is an example of the original setup. Use your own software path and check the current installation guide.',
                     body='<p>See the <a href="https://chtc.cs.wisc.edu/uw-research-computing/hpc-software" target="_blank" rel="noopener noreferrer">HPC software guide ↗</a> for installation policies. HTC jobs need a portable environment or container; see the <a href="https://chtc.cs.wisc.edu/uw-research-computing/conda-installation" target="_blank" rel="noopener noreferrer">HTC Conda guide ↗</a>.</p>'),
             section('Submit a Slurm job', 'An sbatch file describes the resources and the command to run. Save this example as submit_job.sh and adapt it before submitting.', 'submit_job.sh',
                     note='This is a submission template. Choose CPU, memory, runtime, and partition requests that match the application; the template does not make a serial Python program parallel.'),
             section('Monitor and inspect results', 'Check queue status and job accounting, then inspect the output and error logs. Use the HTC commands when your workload runs under HTCondor.', 'monitor_jobs.sh', images=[('hpc_image/resource.png','Original computing-resource illustration')],
                     body='<dl class="lesson-definitions"><div><dt>Node</dt><dd>A compute server containing processors, memory, and other hardware.</dd></div><div><dt>CPU and core</dt><dd>A CPU contains cores. Match Slurm CPU requests to how the application uses processes or threads.</dd></div></dl>'),
             section('Terminal command reference', 'Keep everyday navigation, inspection, archive, compilation, and environment commands close at hand.', 'shell_reference.sh', images=[('hpc_image/alias.png','Original shell-alias examples')],
                     note='Edit aliases for your own access point and reload the appropriate shell configuration. Use the official CHTC login guide for authentication setup.')],
         resources=[('CHTC login guide','https://chtc.cs.wisc.edu/uw-research-computing/connecting'),('Slurm submission guide','https://chtc.cs.wisc.edu/uw-research-computing/hpc-job-submission'),('HTC job submission','https://chtc.cs.wisc.edu/uw-research-computing/htcondor-job-submission')]),
    dict(id='vcs', title='Git & GitHub for research', category='Computing',
         intro='Keep research code organized, record changes clearly, and work with branches and large files using a reproducible version-control workflow.',
         tags=['Git', 'GitHub', 'Git LFS'], level='Terminal basics', flow=['Edit', 'Commit', 'Share'],
         goals=['Connect a local repository to GitHub.', 'Record changes and compare development branches.', 'Track large files and reproduce a historical model version.'],
         prep=['Git installed and a GitHub account.', 'Git LFS for the large-file section.', 'Replace example repository names, email addresses, and paths with your own.'],
         sections=[
             section('Connect to GitHub', 'Create an SSH key if you need one, add the public key to your GitHub account, then test the connection.', 'github_connection.sh',
                     body='<p>Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent" target="_blank" rel="noopener noreferrer">GitHub’s SSH setup instructions ↗</a> for adding the key to the agent and account.</p>'),
             section('Record and share changes', 'Clone the repository, review the working tree, stage the files you intend to publish, and create a descriptive commit.', 'record_changes.sh',
                     note='A clone already has an origin remote. For a new local repository, set its remote URL once before the first push.'),
             section('Work with branches', 'Create a branch for a change, commit there, and merge it into the main branch after review.', 'branch_workflow.sh',
                     body='<div class="lesson-branch" role="img" aria-label="Main branch continues while a feature branch records a change and merges back"><span>main</span><i></i><span>feature</span><i></i><span>merge</span></div>'),
             section('Manage large files with Git LFS', 'Track a file pattern, commit the .gitattributes file, and add the large file. LFS stores a pointer in Git and manages the file content separately.', 'large_files.sh',
                     note='Quote filenames containing spaces. Collaborators need Git LFS installed to retrieve the tracked file content.'),
             section('Reproduce a CLM model version', 'Use the original Arctic carbon-cycle update example to compare a version containing the updates with the version immediately before them.', 'clm_versions.sh',
                     images=[('vcs_image/github_update_requests.png','Arctic carbon-cycle update commits'),('vcs_image/git_clone.png','Clone the model repository'),('vcs_image/git_checkout.png','Select the updated model version'),('vcs_image/git_log.png','Inspect the commit history'),('vcs_image/final.png','Compare the model-version branches')],
                     note='The commit identifiers are from the original CLM/CTSM example. Confirm that they exist in the repository you clone; branch names in the screenshots may differ.')],
         resources=[('GitHub SSH documentation','https://docs.github.com/en/authentication/connecting-to-github-with-ssh'),('Git LFS configuration','https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage'),('Git branching','https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging')])
]

NEW_CODE = {
 'rs_data_processing/geotiff_usage.py': '''from read_write_geotiff import read_tif, array_to_geotiff

array, transform, projection, rows, cols = read_tif("data/imagery.tif")
if array.ndim == 2:
    array = array[..., None]
array_to_geotiff(array, "data/imagery_copy.tif", transform, projection)
print(rows, cols, array.shape)
''',
 'hpc/connect_and_transfer.sh': '''# Local terminal: replace YOUR_NETID with your account name.
ssh YOUR_NETID@spark-login.chtc.wisc.edu

# Copy a file to your home directory (run from the local terminal).
scp input.csv YOUR_NETID@spark-login.chtc.wisc.edu:/home/YOUR_NETID/

# Copy results back to the current local directory.
scp YOUR_NETID@spark-login.chtc.wisc.edu:/scratch/YOUR_NETID/results.zip .
''',
 'hpc/python_environment.sh': '''# Run after installing Conda according to the CHTC guide.
conda env list
conda create -n research python=3.11
conda activate research
conda install numpy pandas matplotlib
conda env export > environment.yml
conda deactivate
# Run the analysis through a compute job, using the next section.
''',
 'hpc/submit_job.sh': '''#!/bin/bash
#SBATCH --job-name=research_example
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=research_%j.out
#SBATCH --error=research_%j.err

# Replace the Conda installation, environment, and analysis paths.
source /path/to/miniconda3/etc/profile.d/conda.sh
conda activate research
cd /scratch/YOUR_NETID/project
python analysis.py
''',
 'hpc/monitor_jobs.sh': '''# Slurm: submit, inspect the queue, and review accounting.
sbatch submit_job.sh
squeue -u "$USER"
sacct -j JOB_ID --format=JobID,State,Elapsed,MaxRSS

# Inspect the logs for your job.
cat research_JOB_ID.out
cat research_JOB_ID.err

# HTCondor: run on your assigned HTC access point.
condor_q
condor_status
''',
 'hpc/shell_reference.sh': '''# Navigate and inspect files.
pwd
cd project
ls -lh
cat notes.txt
readlink -f notes.txt
wc -l notes.txt
grep "pattern" notes.txt
echo "A B B A C C" > example.txt
python3 wc.py example.txt

# Archives: write an archive outside the directory being archived.
zip -r example.zip example/
unzip -l example.zip
unzip example.zip
tar -cvf data.tar data_folder/
tar -xvf data.tar -C destination/
tar -xzf data.tar.gz -C destination/

# Compile and run the original ecosystem-model example.
g++ xtem423e4.cpp -o temmodel
./temmodel tem4.para tem4.log
module avail
make

# Shell configuration and aliases.
nano ~/.bashrc
source ~/.bashrc
# On macOS with Zsh, use ~/.zshrc instead.

# Conda environment management.
conda env list
conda activate research
conda deactivate

# Interactive Slurm testing (adapt the resource request).
srun --partition=int --nodes=1 --ntasks=1 --cpus-per-task=4 --time=00:30:00 --pty bash

# In the vi editor: :wq saves and exits; :q! exits without saving.
''',
 'vcs/github_connection.sh': '''# Create a key only if you do not already have a suitable one.
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add the PUBLIC .pub key to GitHub using its SSH setup guide.
# Then test the connection.
ssh -T git@github.com
''',
 'vcs/record_changes.sh': '''git clone git@github.com:YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
git status
git diff
git add README.md
git commit -m "Describe the change"
git push origin main

# For a new local repository, rather than an existing clone:
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPOSITORY.git
# git push -u origin main
''',
 'vcs/branch_workflow.sh': '''git switch -c feature-analysis
# Edit your analysis, then review and record the changes.
git diff
git add analysis.py
git commit -m "Add analysis workflow"
git push -u origin feature-analysis

# After review, merge the branch into main.
git switch main
git merge feature-analysis
git push origin main
git branch -d feature-analysis
''',
 'vcs/large_files.sh': '''git lfs install
git lfs track "data/large_file.zip"
git add .gitattributes
git add "data/large_file.zip"
git commit -m "Track research archive with Git LFS"
git push origin main

# After cloning a repository that uses LFS:
git lfs ls-files
git lfs pull
''',
 'vcs/clm_versions.sh': '''git clone https://github.com/ESCOMP/CTSM.git
cd CTSM
git log --oneline

# Updated version in the original example.
git switch -c abz_updates dd0cbec
git log --oneline -5

# Version before the original update series.
git switch -c no_abz 384c726
git branch
git diff no_abz..abz_updates
'''
}

def original_codes(source):
    result=[]
    for block in re.findall(r'<pre\b[^>]*>(.*?)</pre>',source,re.S):
        match=re.search(r'<code\b[^>]*>(.*?)</code>',block,re.S)
        if match:
            result.append(unescape(match.group(1)))
    return result

def repair_scatter_indentation(text):
    text=text.replace('def d(x,y):\nxy = np.vstack([x,y])\nz = gaussian_kde(xy)(xy)\nreturn z','def d(x,y):\n    xy = np.vstack([x,y])\n    z = gaussian_kde(xy)(xy)\n    return z')
    lines=text.splitlines(keepends=True)
    start=next(i for i,line in enumerate(lines) if line.startswith('for tr in '))
    end=next(i for i,line in enumerate(lines[start:],start) if line.startswith('plt.savefig'))
    lines[start]='    '+lines[start]
    for i in range(start+1,end):
        if lines[i].strip():lines[i]='        '+lines[i]
    return ''.join(lines)

def image_figure(src, caption, hero=False):
    from PIL import Image
    file=PAGES / src
    with Image.open(file) as im: width,height=im.size
    dark=Path(src).name in {'trait_covariance.png','seasonal_variation.png','PFT_extra.png'}
    bg='#252a34' if dark else '#ffffff'
    return f'''<figure class="lesson-figure{' lesson-figure-hero' if hero else ''}">
      <button type="button" class="lesson-image-button" data-lesson-image data-image-src="{escape(src)}" data-image-caption="{escape(caption)}" data-image-background="{bg}" aria-label="Enlarge figure: {escape(caption)}" style="--figure-background:{bg}">
        <img src="{escape(src)}" width="{width}" height="{height}" alt="{escape(caption)}" {'fetchpriority="high"' if hero else 'loading="lazy"'} decoding="async">
        <span class="lesson-enlarge" aria-hidden="true">↗</span>
      </button><figcaption>{escape(caption)} · Click to enlarge</figcaption></figure>'''

def code_card(guide, item):
    if not item['filename']: return ''
    filename=item['filename']; file=CODE / guide['id'] / filename
    text=file.read_text(); display=text
    parameters=''
    match=re.match(r'^\s*"""(.*?)"""\s*',text,re.S)
    if match:
        parameters=f'<details class="lesson-parameters"><summary>Parameters &amp; layout notes</summary><pre>{escape(match.group(1).strip())}</pre></details>'
        display=text[match.end():]
    language='python' if filename.endswith('.py') else 'bash'
    lines=len(display.splitlines()); collapsed=lines>24
    path=f'../../assets/code/tutorials/{guide["id"]}/{filename}'
    return parameters+f'''<div class="lesson-code{' is-collapsed' if collapsed else ''}" data-code-card>
      <div class="lesson-code-toolbar"><span class="lesson-code-filename">{escape(filename)}</span><span class="lesson-code-language">{'Python' if language=='python' else 'Shell'}</span>
      <div class="lesson-code-actions"><button type="button" data-code-wrap aria-pressed="false" aria-label="Toggle line wrapping for {filename}">Wrap</button><button type="button" data-code-copy aria-label="Copy {filename}">Copy</button><a href="{path}" download aria-label="Download {filename}">↓</a></div></div>
      <pre class="lesson-code-scroll" tabindex="0" aria-label="{filename} code"><code class="language-{language}">{escape(display)}</code></pre>
      <template data-code-source>{escape(text)}</template>
      {f'<button class="lesson-code-expand" type="button" data-code-expand aria-expanded="false">Expand code · {lines} lines <span aria-hidden="true">↓</span></button>' if collapsed else ''}
      <span class="lesson-code-status" data-code-status role="status" aria-live="polite"></span></div>'''

def link(label, href):
    extra=' target="_blank" rel="noopener noreferrer"' if href.startswith('http') else ''
    return f'<a href="{escape(href)}"{extra}>{escape(label)} <span aria-hidden="true">↗</span></a>'

def article_content(guide, index):
    tags=''.join(f'<span>{escape(tag)}</span>' for tag in guide['tags'])
    sections=[]; toc=[]
    for number,item in enumerate(guide['sections'],1):
        section_id=f'lesson-{number}'
        toc.append(f'<a href="#{section_id}" data-lesson-toc><span>{number:02d}</span>{escape(item["title"])}</a>')
        images=''.join(image_figure(*img) for img in item['images'])
        gallery=f'<div class="lesson-figures{ " lesson-figures-multiple" if len(item["images"])>1 else ""}">{images}</div>' if images else ''
        note=f'<aside class="lesson-note"><span>Keep in mind</span><p>{escape(item["note"])}</p></aside>' if item['note'] else ''
        sections.append(f'<section class="lesson-section" id="{section_id}" aria-labelledby="{section_id}-title"><div class="lesson-section-heading"><span class="lesson-step">{number:02d}</span><h3 id="{section_id}-title">{escape(item["title"])}</h3></div><p class="lesson-section-intro">{escape(item["description"])}</p>{item["body"]}{gallery}{code_card(guide,item)}{note}</section>')
    if guide.get('hero'):
        visual=image_figure(guide['hero'],'Example output',True)
    else:
        visual='<div class="lesson-flow" role="img" aria-label="'+escape(' to '.join(guide['flow']))+'">'+''.join(f'<span class="lesson-flow-step"><b>{i:02d}</b>{escape(value)}</span>' for i,value in enumerate(guide['flow'],1))+'</div>'
    goals=''.join(f'<li>{escape(x)}</li>' for x in guide['goals'])
    prep=''.join(f'<li>{escape(x)}</li>' for x in guide['prep'])
    previous=GUIDES[index-1] if index else None
    following=GUIDES[index+1] if index+1<len(GUIDES) else None
    prev=f'<a href="./{previous["id"]}.html"><span>← Previous tutorial</span><strong>{escape(previous["title"])}</strong></a>' if previous else '<a href="../tutorials.html"><span>← Tutorial library</span><strong>Explore all guides</strong></a>'
    nxt=f'<a href="./{following["id"]}.html"><span>Next tutorial →</span><strong>{escape(following["title"])}</strong></a>' if following else '<a href="../tutorials.html"><span>Tutorial library →</span><strong>Explore all guides</strong></a>'
    resources=''.join(link(*x) for x in guide['resources'])
    return f'''<header class="lesson-header"><a class="lesson-back" href="../tutorials.html">← All tutorials</a><p class="lesson-eyebrow">{escape(guide['category'])} · Practical guide</p><h2 class="lesson-title">{escape(guide['title'])}</h2></header>
    <div class="lesson-hero"><div class="lesson-hero-copy"><p>{escape(guide['intro'])}</p><div class="lesson-tags">{tags}</div><a class="lesson-start" href="#lesson-1">Start learning <span aria-hidden="true">↓</span></a></div>{visual}</div>
    <div class="lesson-preparation"><details open><summary>What you’ll learn</summary><ul>{goals}</ul></details><details><summary>Before you begin <span>{escape(guide['level'])}</span></summary><ul>{prep}</ul></details></div>
    <div class="lesson-layout"><aside class="lesson-toc"><details data-lesson-outline><summary>On this page <span>{len(sections)} sections</span></summary><nav aria-label="Tutorial chapters">{''.join(toc)}</nav></details></aside><div class="lesson-content">{''.join(sections)}</div></div>
    <section class="lesson-resources" aria-labelledby="lesson-resources-title"><h3 id="lesson-resources-title">Keep exploring</h3><div>{resources}</div><a class="lesson-bundle" href="../../assets/code/tutorials/{guide['id']}/examples.zip" download>Download all examples <span aria-hidden="true">↓</span></a></section>
    <nav class="lesson-next" aria-label="Adjacent tutorials">{prev}{nxt}</nav>'''

IMAGE_DIALOG='''<dialog class="lesson-image-viewer" data-lesson-viewer aria-labelledby="lesson-image-title">
  <header><h2 id="lesson-image-title">Figure</h2><button type="button" data-image-close aria-label="Close figure viewer">✕</button></header>
  <div class="lesson-image-tools"><button type="button" data-image-fit>Fit screen</button><button type="button" data-image-read>Zoom in</button><a data-image-original target="_blank" rel="noopener noreferrer">Open original ↗</a></div>
  <div class="lesson-image-stage" data-image-stage tabindex="0" aria-label="Figure; zoom in and scroll to explore"><img data-image-full alt=""></div>
</dialog>'''

def build(original_directory=None):
    changes=[]
    for guide in GUIDES:
        folder=CODE/guide['id'];folder.mkdir(parents=True,exist_ok=True)
        path=PAGES/(guide['id']+'.html')
        source=(original_directory/path.name).read_text() if original_directory else path.read_text()
        imported=original_codes(source) if original_directory else []
        for item in guide['sections']:
            filename=item['filename']
            if not filename:continue
            file=folder/filename
            if item['original'] is not None and original_directory:
                text=imported[item['original']]
                if guide['id']=='scatter_line_plot' and item['original']==0:
                    text=repair_scatter_indentation(text)
                file.write_text(text)
            elif guide['id']+'/'+filename in NEW_CODE:
                file.write_text(NEW_CODE[guide['id']+'/'+filename])
            elif not file.exists():raise RuntimeError(f'Missing example: {file}')
        readme=f"{guide['title']}\n\n{guide['intro']}\n\nBefore you begin:\n"+'\n'.join('- '+s for s in guide['prep'])+'\n\nExamples are intended for adaptation. Research-specific datasets are not bundled.\n'
        (folder/'README.txt').write_text(readme)
        with zipfile.ZipFile(folder/'examples.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(folder.iterdir()):
                if file.suffix in {'.py','.sh','.txt'}:archive.write(file,file.name)
        start=source.index('<article class="tutorial')
        footer_start=source.index('<footer ',start)
        prefix=source[:start]
        prefix=re.sub(r'<style>.*?</style>','',prefix,flags=re.S)
        prefix=re.sub(r'<link[^>]+href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/[^>]+>','',prefix)
        prefix=re.sub(r'<link[^>]+href="../../assets/css/tutorial-reader.css[^>]*>','',prefix)
        prefix=re.sub(r'<meta name="description"[^>]*>','',prefix)
        prefix=prefix.replace('<body>', '<body class="tutorial-document">')
        theme=re.search(r'<button class="theme-toggle-btn".*?</button>',prefix,re.S)
        if theme:
            button=theme.group().replace(' data-desktop-only','')
            prefix=prefix[:theme.start()]+prefix[theme.end():]
            prefix=prefix.replace('<aside class="sidebar" data-sidebar>', '<aside class="sidebar" data-sidebar>\n'+button)
        if 'highlight.min.js' not in prefix:
            prefix=prefix.replace('</head>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/highlight.min.js" defer></script>\n</head>')
        prefix=re.sub(r'<title>.*?</title>',f'<title>{escape(guide["title"])} | Fujiang Ji</title>',prefix)
        prefix=prefix.replace('</head>',f'<meta name="description" content="{escape(guide["intro"])}">\n<link rel="stylesheet" href="../../assets/css/tutorial-reader.css?v={VERSION}">\n</head>')
        tail=source[footer_start:]
        tail=re.sub(r'<script>.*?</script>',lambda m:'' if ('copyText' in m.group() or 'hljs' in m.group()) else m.group(),tail,flags=re.S)
        tail=re.sub(r'<dialog class="lesson-image-viewer".*?</dialog>','',tail,flags=re.S)
        tail=re.sub(r'<script src="../../assets/js/tutorial-reader.js[^>]*></script>','',tail)
        tail=tail.replace('</body>',IMAGE_DIALOG+'\n<script src="../../assets/js/tutorial-reader.js?v=20261009-i18n90" defer></script>\n</body>')
        result=prefix+'<article class="tutorial tutorial-reader active" data-page="tutorial">\n'+article_content(guide,GUIDES.index(guide))+'\n'+tail
        path.write_text(result)
        changes.append(dict(page=path.relative_to(ROOT).as_posix(),code=[dict(file=(folder/i['filename']).relative_to(ROOT).as_posix(),sha256=hashlib.sha256((folder/i['filename']).read_bytes()).hexdigest()) for i in guide['sections'] if i['filename']]))
    (CODE/'SOURCES.json').write_text(json.dumps(dict(version=VERSION,guides=changes,notes=['Research plotting examples originate from the six existing tutorial pages.','The density-scatter helper indentation was corrected.','HPC and Git examples were reorganized and corrected with links to official documentation.','Research figures remain unchanged in their original directories.']),indent=2)+'\n')
    print('Built six tutorial readers and their downloadable examples.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--original-directory',type=Path)
    args=parser.parse_args()
    build(args.original_directory)
