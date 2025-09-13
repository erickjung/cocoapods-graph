# frozen_string_literal: true

module CocoaPodsGraph
  # Project metadata constants - single source of truth
  PROJECT_NAME = 'cocoapods-graph'
  PROJECT_DESCRIPTION = 'Generate interactive dependency graphs for CocoaPods projects'
  PROJECT_AUTHOR = 'Erick Jung'
  PROJECT_EMAIL = 'talk@erickjung.com'
  PROJECT_HOMEPAGE = 'https://github.com/erickjung/cocoapods-graph'
  PROJECT_SOURCE_CODE_URI = 'https://github.com/erickjung/cocoapods-graph'
  PROJECT_CHANGELOG_URI = 'https://github.com/erickjung/cocoapods-graph/blob/main/CHANGELOG.md'
  PROJECT_LICENSE = 'MIT'
  
  # Derived constants for convenience
  PROJECT_AUTHOR_WITH_EMAIL = "#{PROJECT_AUTHOR} (#{PROJECT_EMAIL})"
  PROJECT_SUMMARY = 'Interactive dependency wheel visualizations for CocoaPods projects'
end
