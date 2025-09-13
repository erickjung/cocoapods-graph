require_relative "lib/cocoapods_graph/version"
require_relative "lib/cocoapods_graph/constants"

Gem::Specification.new do |spec|
  spec.name          = CocoaPodsGraph::PROJECT_NAME
  spec.version       = CocoaPodsGraph::VERSION
  spec.authors       = [CocoaPodsGraph::PROJECT_AUTHOR]
  spec.email         = [CocoaPodsGraph::PROJECT_EMAIL]

  spec.summary       = CocoaPodsGraph::PROJECT_SUMMARY
  spec.description   = "A Ruby gem that parses Podfile.lock files and generates beautiful, interactive dependency wheel visualizations using D3.js. Perfect for understanding complex pod relationships in your iOS projects."
  spec.homepage      = CocoaPodsGraph::PROJECT_HOMEPAGE
  spec.license       = CocoaPodsGraph::PROJECT_LICENSE
  spec.required_ruby_version = ">= 2.6.0"

  spec.metadata["allowed_push_host"] = "https://rubygems.org"
  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = CocoaPodsGraph::PROJECT_SOURCE_CODE_URI
  spec.metadata["changelog_uri"] = CocoaPodsGraph::PROJECT_CHANGELOG_URI

  # Specify which files should be added to the gem when it is released.
  spec.files = Dir.chdir(File.expand_path(__dir__)) do
    Dir.glob("lib/**/*") + Dir.glob("exe/*") + %w[
      cocoapods-graph.gemspec
      README.md
      LICENSE
      CHANGELOG.md
      Gemfile
      Rakefile
    ]
  end
  
  spec.bindir        = "exe"
  spec.executables   = ["cocoapods-graph"]
  spec.require_paths = ["lib"]

  # Runtime dependencies
  spec.add_dependency "json", "~> 2.0"

  # Development dependencies
  spec.add_development_dependency "bundler", "~> 2.0"
  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.0"
end
