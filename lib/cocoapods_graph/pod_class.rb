module CocoaPodsGraph
  class PodClass
    attr_accessor :name, :version, :dependencies

    def initialize(name, version, dependencies)
      @name = name
      @version = version
      @dependencies = dependencies
    end

    def print_object
      puts "#{@name} #{@version}"
      @dependencies.each do |dep|
        puts "  #{dep.name} #{dep.version}"
      end
    end
  end
end
