require 'bundler/gem_tasks'
require 'rspec/core/rake_task'

RSpec::Core::RakeTask.new(:spec)

desc 'Run tests'
task default: :spec

desc 'Install gem locally'
task :install_local do
  sh 'gem build cocoapods-graph.gemspec'
  sh 'gem install cocoapods-graph-*.gem'
end

desc 'Uninstall gem'
task :uninstall do
  sh 'gem uninstall cocoapods-graph'
end
