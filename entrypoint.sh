#!/bin/sh

command=$1

IMAGE_DIR=docs/assets/images

# Generate code reference pages
python3 scripts/generate_code_reference_pages.py

# Generate Terraform docs
python3 scripts/generate_terraform_docs.py

# Generate infrastructure diagrams
mkdir -p ${IMAGE_DIR}

for project in $(find terraform/ -mindepth 1 -maxdepth 1); do
    echo "[*] Generating diagram image for: ${project}"

    inframap generate ${project} | dot -Tpng > ${IMAGE_DIR}/${project//\//_}.png
done

# Clean up any failed images
find ${IMAGE_DIR} -empty -not -name .keep -print0 | xargs -0 rm -f

case $command in
    build)
        # Build static web pages
        exec mkdocs build -v
        ;;
    serve)
        # Serve pages with live-reload
        exec mkdocs serve
        ;;
    *|sh)
        echo "[*] Please specify 'build' or 'serve'"
        exec /bin/sh
        ;;
esac
