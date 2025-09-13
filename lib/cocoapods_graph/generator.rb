require 'json'
require 'time'

module CocoaPodsGraph
  class Generator

    def self.parse_lock_file(file_name)
      def self.parse_lock_pods_line(line)
        begin
          name = line[line.index('-') + 1...line.index('(')].strip
        rescue
          name = line[line.index('-') + 1..-1].strip
        end

        begin
          version = line[line.index('(') + 1...line.index(')')].strip
        rescue
          version = ''
        end

        PodClass.new(name, version, [])
      end

      content_file = File.readlines(file_name).map { |x| x.chomp.delete('"') }

      result_list = []
      pod = PodClass.new('', '', [])
      
      content_file.each do |line|
        if line.start_with?('  -')
          result_list << pod if pod.name.length > 0
          pod = parse_lock_pods_line(line)
        elsif line.start_with?('    -')
          pod.dependencies << parse_lock_pods_line(line)
        elsif line.start_with?('DEPENDENCIES')
          result_list << pod if pod.name.length > 0
          break
        end
      end

      result_list
    end

    def self.generate_json(result_list)
      def self.generate_json_deps(result_list)
        data = '{'
        result_list.each do |result|
          data += '"%s":"1",' % [result.name]
        end
        data = data[0...-1]
        data + '}'
      end

      json = '{"packages": ['
      deps = generate_json_deps(result_list)
      json += '{"name":"app","require":%s},' % deps

      result_list.each do |pod|
        if pod.dependencies.length > 0
          pod_deps = generate_json_deps(pod.dependencies)
          json += '{"name":"%s","require":%s},' % [pod.name, pod_deps]
        else
          json += '{"name":"%s","require":{}},' % pod.name
        end
      end

      json[0...-1] + ']}'
    end

    def self.save_json_file(data, file_name)
      File.open(file_name + '.json', 'w') do |outfile|
        outfile.write(generate_json(data))
      end
    end

    def self.save_html_wheel_file(data, file_name)
      template_path = File.join(__dir__, 'template.html')
      p_template = File.read(template_path)
      p_data_json = "'%s'" % generate_json(data)
      p_data_width = '960'
      p_data_margin = '200'
      p_data_padding = '.02'
      p_generation_date = Time.now.strftime('%B %d, %Y at %I:%M %p')

      html_out = p_template.gsub('P_DATA_JSON', p_data_json)
                          .gsub('P_DATA_WIDTH', p_data_width)
                          .gsub('P_DATA_MARGIN', p_data_margin)
                          .gsub('P_DATA_PADDING', p_data_padding)
                          .gsub('P_GENERATION_DATE', p_generation_date)

      File.open(file_name + '.html', 'w') do |outfile|
        outfile.write(html_out)
      end
    end
  end
end
