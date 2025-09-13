require_relative '../lib/cocoapods_graph'

RSpec.describe CocoaPodsGraph do
  it "has a version number" do
    expect(CocoaPodsGraph::VERSION).not_to be nil
  end
end
